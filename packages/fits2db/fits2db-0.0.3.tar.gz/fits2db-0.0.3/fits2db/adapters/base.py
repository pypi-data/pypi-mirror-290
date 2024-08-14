"""
This module defines the BaseLoader class, an abstract base class for handling
the loading of data from FITS files into a database. The class provides
functionality to write metadata about the FITS files and their corresponding
tables into the database and offers abstract methods for custom data
operations such as dropping tables and upserting data.

Classes:
    BaseLoader: An abstract base class for writing data from FITS files into a database.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

import pandas as pd
from sqlalchemy import engine, MetaData, Table, text, inspect
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError

from ..config.config_model import ConfigType
from ..fits.fits import FitsFile
from .meta import Base, Fits2DbMeta, Fits2DbTableMeta

log = logging.getLogger("fits2db")


class BaseLoader(ABC):
    """
    An abstract base class for writing data from FITS files into a database.

    Attributes:
        db_url (str): The database URL.
        engine (engine.Engine): The SQLAlchemy engine for the database.
        config (ConfigType): Configuration data for loading tables from the FITS file.
        file (FitsFile): The FITS file object containing data to be loaded.
        session (Session): SQLAlchemy session object for database transactions.
        new_file (Fits2DbMeta): Metadata object for the FITS file.
        db_table_names (set): Set of table names currently in the database.
    """

    def __init__(
        self, db_url: str, engine: engine, config: ConfigType, file: FitsFile
    ):
        """
        Initializes the BaseLoader with the given database URL, engine, configuration, and FITS file.

        Args:
            db_url (str): The database URL.
            engine (engine.Engine): The SQLAlchemy engine for the database.
            config (ConfigType): Configuration data for loading tables from the FITS file.
            file (FitsFile): The FITS file object containing data to be loaded.
        """
        self.db_url = db_url
        self.engine = engine
        self.config = config
        self.file = file

    @abstractmethod
    def create_db_url(self) -> str:
        pass

    def db_session(self) -> Session:
        """
        Creates and returns a new SQLAlchemy session for the database.

        Returns:
            Session: A new SQLAlchemy session object.
        """
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        return Session()

    def write_file_meta(self, session: Session) -> None:
        """
        Writes metadata about the FITS file to the database.
        """
        log.debug(f"Filepath {self.file.absolute_path.as_posix()}")
        self.new_file = Fits2DbMeta(
            filename=self.file.file_name,
            filepath=self.file.absolute_path.as_posix(),
            last_file_mutation=self.file.mdate,
        )
        session.add(self.new_file)
        session.commit()

    def write_table_meta(
        self, tbl_name: str, df: pd.DataFrame, session: Session, file_id: int
    ) -> None:
        """
        Writes metadata about a table in the FITS file to the database.

        Args:
            tbl_name (str): The name of the table.
            df (pd.DataFrame): The DataFrame representing the table data.
        """
        rows, cols = df.shape
        new_table = Fits2DbTableMeta(
            file_meta_id=file_id,
            tablename=tbl_name,
            record_count=rows,
            column_count=cols,
        )
        session.add(new_table)
        session.commit()

    def get_tables(self, session: Session) -> set[str]:
        """
        Retrieves and stores the names of all tables currently in the database.
        """
        db_table_names = session.execute(
            select(Fits2DbTableMeta.tablename)
        ).fetchall()
        db_table_names = [name[0] for name in db_table_names]
        return set(db_table_names)

    def drop_user_tables(self, session: Session) -> None:
        """
        Drops FITS2DB created data tables from the database if they exist.
        """
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        log.info(metadata.tables)
        try:
            db_table_names = self.get_tables(session)
            for table_name in db_table_names:
                if table_name in metadata.tables:
                    metadata.tables[table_name].drop(self.engine)
                    log.info(f"Dropped table {table_name}")
                if table_name + "_META" in metadata.tables:
                    metadata.tables[table_name + "_META"].drop(self.engine)
                    log.info(f"Dropped table {table_name+'_META'}")
                if "TMP_" + table_name in metadata.tables:
                    metadata.tables["TMP_" + table_name].drop(self.engine)
                    log.info(f"Dropped table {'TMP_'+table_name}")

        except SQLAlchemyError as e:
            log.error(f"An error occurred while dropping tables: {e}")
        finally:
            self.engine.dispose()

    def delete_meta_tables(self, session: Session) -> None:
        """
        Drops FITS2DB created data tables from the database if they exist.
        """
        log.debug("Start deletion of Meta tables")
        try:
            session.query(Fits2DbTableMeta).delete()
            log.debug("Run delete stmt for Fits2DbTableMeta")
            session.query(Fits2DbMeta).delete()
            log.debug("Commit changes")
            session.commit()
        except SQLAlchemyError as err:
            log.error(err)

    def clean_db(self) -> None:
        """
        Cleans the database by dropping specific tables and metadata tables.
        """
        with self.db_session() as session:
            self.drop_user_tables(session)
            self.delete_meta_tables(session)

    def get_fits2db_meta(self) -> pd.DataFrame:
        """
        Retrieves the FITS2DB_META table from the database and returns it as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the FITS2DB_META table data.
        """
        try:
            df = pd.read_sql_table("FITS2DB_META", con=self.engine)
            return df
        except Exception as err:
            log.error(err)
            raise

    def upload_file(self) -> None:
        """
        Upserts the FITS file and its tables into the database.
        """
        with self.db_session() as session:
            self.write_file_meta(session)
            table_configs = self.config["fits_files"]["tables"]
            log.debug("Start upserting data")

            for table in table_configs:
                log.debug(f"Table in configs: {table}")
                table_name = table["name"]
                log.info(table_name)
                log.info(table["ingest_all_columns"])
                try:
                    df = self.file.get_table(table_name)
                    df.data["FILE_META_ID"] = self.new_file.id
                    df.data.columns = map(str.upper, df.data.columns)
                    df.meta.columns = map(str.upper, df.meta.columns)
                    self.write_table_meta(
                        table_name, df.data, session, self.new_file.id
                    )
                    self.upsert_data_table(table_name, df.data)
                    self.update_table(table_name + "_META", df.meta)
                except KeyError as err:
                    log.error(f"\n {err}")

    def update_fits2db_meta(self, session: Session) -> Fits2DbMeta:
        file_record = (
            session.query(Fits2DbMeta)
            .filter_by(
                filepath=self.file.absolute_path.as_posix(),
                filename=self.file.file_name,
            )
            .first()
        )
        if file_record is None:
            log.error(
                f"No record found for file: {self.file.file_name} at {self.file.absolute_path.as_posix()}"
            )
            return
        file_record.last_file_mutation = self.file.mdate
        return file_record

    def update_fits2db_table(self, session: Session, file_record: Fits2DbMeta):
        tables_to_delete = session.query(Fits2DbTableMeta).filter(
            Fits2DbTableMeta.file_meta_id == file_record.id
        )
        for table_meta in tables_to_delete:
            tablename = table_meta.tablename
            metadata = MetaData()
            table = Table(tablename, metadata, autoload_with=self.engine)
            delete_stmt = table.delete().where(
                table.c.FILE_META_ID == file_record.id
            )
            session.execute(delete_stmt)
            log.info(
                f"Deleted rows in table '{tablename}' where file_meta_id = {file_record.id}"
            )

        tables_to_delete.delete(synchronize_session=False)

    def update_file(self) -> None:
        """
        Updates the metadata and data of the FITS file in the database.
        """
        with self.db_session() as session:
            file_record = self.update_fits2db_meta(session)
            self.update_fits2db_table(session, file_record)
            session.commit()
            table_configs = self.config["fits_files"]["tables"]
            log.debug("Start upserting data")

            for table in table_configs:
                log.debug(f"Table in configs: {table}")
                table_name = table["name"]
                log.info(table_name)
                log.info(table["ingest_all_columns"])
                try:
                    df = self.file.get_table(table_name)
                    df.data["FILE_META_ID"] = file_record.id
                    df.data.columns = map(str.upper, df.data.columns)
                    df.meta.columns = map(str.upper, df.meta.columns)
                    self.write_table_meta(
                        table_name, df.data, session, file_record.id
                    )
                    self.upsert_data_table(table_name, df.data)
                    self.update_table(table_name + "_META", df.meta)
                except KeyError as err:
                    log.error(f"\n {err}")

    def upsert_data_table(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Upserts data into a table in the database. If the table exists, merges the data.
        Otherwise, renames the temporary table.

        Args:
            table_name (str): The name of the table to upsert.
            df (pd.DataFrame): The DataFrame containing the data to upsert.
        """
        log.debug("Passed engine:")
        log.debug(self.engine)
        try:
            tmp_tbl = "TMP_" + table_name
            with self.engine.connect() as conn:
                df.to_sql(
                    name=tmp_tbl,
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                log.info(f"Temporary table {tmp_tbl} created.")

            if self.check_table_exists(table_name):
                self.merge_tables(table_name, tmp_tbl)
                self.drop_table(tmp_tbl)
            else:
                self.rename_table(tmp_tbl, table_name)

        except Exception as err:
            log.error(err)
            raise

    def check_table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the database.

        Args:
            table_name (str): The name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        with self.engine.connect() as conn:
            query = text("SHOW TABLES LIKE :table_name")
            result = conn.execute(query, {"table_name": table_name})
            return result.fetchone() is not None

    def drop_table(self, table_name: str) -> bool:
        """
        Drops a table from the database.

        Args:
            table_name (str): The name of the table to drop.

        Returns:
            bool: True if the table was successfully dropped, False otherwise.
        """
        with self.engine.connect() as conn:
            transaction = conn.begin()  # Start a new transaction
            try:
                # Safely create the SQL string with the table name included
                query = text(f"DROP TABLE `{table_name}`")
                conn.execute(query)
                transaction.commit()  # Commit the transaction if the drop is successful
                return True
            except Exception as e:
                transaction.rollback()  # Roll back the transaction on error
                print(f"Failed to drop table {table_name}: {e}")
                return False

    def rename_table(self, old_name: str, new_name: str) -> None:
        """
        Renames a table in the database and adds an auto-incrementing primary key.

        Args:
            old_name (str): The current name of the table.
            new_name (str): The new name for the table.
        """
        with self.engine.connect() as conn:
            try:
                rename_stmt = text(f"RENAME TABLE {old_name} TO {new_name}")
                id_stmt = text(f"""ALTER TABLE {new_name} 
                                ADD COLUMN id INT AUTO_INCREMENT,
                                ADD PRIMARY KEY (id);""")
                conn.execute(rename_stmt)
                conn.execute(id_stmt)
                log.info(
                    f"Table renamed from {old_name} to {new_name} and added primamry key id."
                )
            except SQLAlchemyError as err:
                log.error(err)
                raise

    def execute_sql(self, sql: str) -> None:
        """
        Executes a raw SQL query against the database.

        Args:
            sql (str): The SQL query to execute.
        """
        with self.engine.connect() as conn:
            try:
                conn.execute(text(sql))
                log.info("Query executed successfully")
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                log.error(error)

    def merge_tables(self, original_table: str, tmp_table: str) -> None:
        """
        Merges data from a temporary table into the original table.

        Args:
            original_table (str): The name of the original table.
            tmp_table (str): The name of the temporary table.
        """
        source_table_details = self._fetch_column_details(tmp_table)
        target_table_details = self._fetch_column_details(original_table)
        self._add_missing_columns(
            source_table_details, original_table, target_table_details
        )
        with self.engine.connect() as conn:
            transaction = conn.begin()
            try:
                common_columns = ", ".join(
                    set(source_table_details.keys())
                    & set(target_table_details.keys())
                )
                insert_query = f"""
                INSERT INTO {original_table} ({common_columns})
                SELECT {common_columns}
                FROM {tmp_table}
                """
                result = conn.execute(text(insert_query))
                transaction.commit()  # Commit the transaction
                log.info(
                    f"Data inserted successfully, {result.rowcount} rows affected."
                )
            except Exception as e:
                transaction.rollback()  # Rollback the transaction on error
                log.error(f"An error occurred: {e}")

    def close_connection(self) -> None:
        """
        Closes the database connection pool.
        """
        self.engine.dispose()
        log.info("Database connection pool has been closed.")

    def _fetch_column_details(self, table_name: str) -> Dict[str, Any]:
        """
        Fetches the details of columns in a specified table.

        Args:
            table_name (str): The name of the table to fetch details for.

        Returns:
            Dict[str, Any]: A dictionary mapping column names to their types.
        """
        meta = MetaData()
        table = Table(table_name, meta, autoload_with=self.engine)
        return {column.name: column.type for column in table.columns}

    def _add_missing_columns(
        self,
        source_table_details: Dict[str, Any],
        target_table: str,
        target_table_details: Dict[str, Any],
    ) -> None:
        """
        Adds missing columns to a target table based on the source table's details.

        Args:
            source_table_details (Dict[str, Any]): Details of the source table's columns.
            target_table (str): The name of the target table.
            target_table_details (Dict[str, Any]): Details of the target table's columns.
        """
        with self.engine.connect() as conn:
            for column, col_type in source_table_details.items():
                if column not in target_table_details:
                    alter_query = f"ALTER TABLE {target_table} ADD COLUMN {column} {col_type}"
                    conn.execute(text(alter_query))
                    log.info(
                        f"Added column {column} of type {col_type} to {target_table}"
                    )

    def update_table(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Updates a table in the database by replacing its content with a DataFrame.

        Args:
            table_name (str): The name of the table to update.
            df (pd.DataFrame): The DataFrame containing the data to update.
        """
        log.debug("Passed engine:")
        log.debug(self.engine)
        try:
            tmp_tbl = "TMP_" + table_name
            with self.engine.connect() as conn:
                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="replace",
                    index=False,
                )
                log.info(f"Temporary table {tmp_tbl} created.")

        except Exception as err:
            log.error(err)
            raise
