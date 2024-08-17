import os
import sqlite3

import pandas as pd

from .util import gen_abspath, read_csv


class SQLConnect:

    def __init__(self,
                 db_name: str = 'flameai.db',
                 db_backup_path: str = './'):
        base_path = '/tmp' if os.path.exists('/tmp') else db_backup_path
        self.db_path = gen_abspath(base_path, db_name)
        self.conn = sqlite3.connect(self.db_path)

    def create_table(self,
                     table_name: str,
                     df: pd.DataFrame) -> None:
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

    def create_table_with_csv(self,
                              table_name: str,
                              csv_path: str,
                              sep: str = ',') -> None:
        df = read_csv(file_path=csv_path,
                      sep=sep,
                      header=0)
        self.create_table(table_name, df)

    def sql(self, query) -> pd.DataFrame:
        return pd.read_sql_query(query, self.conn)

    def delete_database(self):
        try:
            os.remove(self.db_path)
        except Exception as e:
            print(f'Can not remove {self.db_path}')
            print(f"Error: {e}")
