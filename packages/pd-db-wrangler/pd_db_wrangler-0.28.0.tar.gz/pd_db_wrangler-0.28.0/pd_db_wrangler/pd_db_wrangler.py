"""Main module."""
import mimetypes
from pathlib import Path

import pandas as pd
import tomllib
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class Pandas_DB_Wrangler:
    """
    Pass connect string with constructor. Connect String may be a path to a
    SQLite database or a path to a ini or text file specifying the database
    connection string. e.g.:
    postgresql+psycopg2://user:passw0rd@dns_name:5432/database_name
    """

    def __init__(self, connect_string=""):
        self.options = {}
        self.sql = None
        if connect_string != "":
            self.connect_string = self.set_connection_string(connect_string)
            self.engine = create_engine(self.connect_string)
        else:
            self.connect_string = ""
            self.engine = None

    def remove_whitespace_around_braces(self, text_to_process: str) -> str:
        """
        SQL Formatters like to pad inline braces with whitespace.
        This function removes the whitespace in front of arguments

        Args:
            text (str): text string with potential whitespace around
            braces

        Returns:
            str: text string with removed whitespace around braces
        """
        return text_to_process.replace("{ ", "{").replace(" }", "}")

    def timezone_setter(self, df: pd.DataFrame, timezone: str) -> pd.DataFrame:
        """Attempts to set the timezone on all specified date columns
        in a dataframe

        Args:
            df (pd.DataFrame): dataframe to process
            timezone (str): timezone

        Returns:
            pd.DataFrame: dataframe with timezones set
        """
        if "datetime" in str(df.index.dtype):
            try:
                df = df.tz_localize(tz=timezone)
            except TypeError as exception:
                if "Already tz-aware" in str(exception):
                    df = df.tz_convert(tz=timezone)
        try:
            if isinstance(self.options["parse_dates"], dict):
                date_list = self.options["parse_dates"].keys()
            elif isinstance(self.options["parse_dates"], list):
                date_list = self.options["parse_dates"]
            elif isinstance(self.options["parse_dates"], str):
                date_list = []
                date_list.append(self.options["parse_dates"])
            for date_col in date_list:
                if date_col in df.columns.values.tolist():
                    try:
                        df[date_col] = df[date_col].dt.tz_localize(tz=timezone)
                    except TypeError as exception:
                        if "Already tz-aware" in str(exception):
                            df[date_col] = df[date_col].dt.tz_convert(tz=timezone)
        except (AttributeError, KeyError) as exception:
            print(exception)
        return df

    def set_connection_string(self, url):
        path = Path(url)
        suffixes = (".db", ".gnucash", ".sqlite")
        if path.exists():
            datatype = mimetypes.guess_type(path)[0]
            if datatype == "text/plain":
                return path.read_text(encoding="utf-8").strip()
            elif datatype == "application/vnd.sqlite3" or path.suffix in suffixes:
                return f"sqlite:///{path}"
        else:
            return url

    def pandas_toml_extractor(self, sql: str) -> str:
        """
        Looks for comments in a SQL file to help pandas determine types.
        Specify date fields under [parse_dates]
        Anything else needing special type handling should go under [dtype]
        Example SQL comment:
        /*pandas*
        timezone = "America/Chicago"
        index_col = ["created_at"]
        [parse_dates]
        created_at = "%Y-%m-%d %H:%M:%S"
        updated_at = "%Y-%m-%d %H:%M:%S"
        [dtype]
        user_name = "string"
        user_id = "int64"
        amt = "float"
        *pandas*/

        Examples of valid ways to pass in parse_dates:
        parse_dates = ["created_at", "delete_comment_date", "edit_comment_date"]
        [parse_dates]
        created_at = "%Y-%m-%d %H:%M:%S"
        updated_at = "%Y-%m-%d %H:%M:%S"
        parse_dates = "created_date"

        Args:
            sql (str): SQL to parse

        Returns:
            str: string containing only the TOML to parse
        """
        toml_text = sql[
            sql.find(start := "/*pandas*") + len(start) : sql.find("*pandas*/")
        ]
        toml_dict = {}
        try:
            toml_dict = tomllib.loads(toml_text)
            if len(toml_dict) > 0:
                # valid toml found, remove it from the sql string
                sql_list = self.sql.split(toml_text)
                self.sql = "".join(sql_list)
        except tomllib.TOMLDecodeError:
            # "No valid toml found in SQL"
            pass
        return toml_dict

    def get_select_stmt(self, sql: str) -> str:
        """Extract the select statement from SQL text

        Args:
            sql (str): Passed in SQL

        Returns:
            str: Select statement of clause
        """
        sql = str(sql).upper()
        select = sql[sql.find(start := "SELECT ") + len(start) : sql.find("FROM ")]
        return "SELECT " + select

    def read_sql_file(self, filename):
        """Read SQL from File"""
        path = Path(filename)
        self.sql = path.read_text(encoding="utf-8")
        self.options = self.pandas_toml_extractor(self.sql)
        self.sql = self.remove_whitespace_around_braces(self.sql)
        return self.sql

    def df_fetch(
        self,
        sql,
        index_col=None,
        parse_dates=None,
        dtype=None,
    ):
        """
        Run SQL query on a database with SQL as a parameter
        Please specify connect string and db type using the
        set_connection_string function.

        Do not re-initialize options unless the select statement changes
        Sometimes where clause will be dynamically injected.
        """
        for key, value in locals().items():
            if key == "sql":
                if self.get_select_stmt(value) != self.get_select_stmt(self.sql):
                    # new sql being passed in, re-initialize options if select stmts differ
                    self.options = {}
            if key not in ("self", "timezone") and value is not None:
                self.options[key] = value
        timezone = self.options.pop("timezone", None)
        with self.engine.begin() as conn:
            df = pd.read_sql(
                con=conn, sql=text(self.options.pop("sql")), **self.options
            )
            if timezone is not None:
                df = self.timezone_setter(df, timezone)
            return df
