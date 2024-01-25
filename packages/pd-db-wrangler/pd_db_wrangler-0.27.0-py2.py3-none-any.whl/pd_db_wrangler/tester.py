from .pd_db_wrangler import Pandas_DB_Wrangler


"""
pdw = Pandas_DB_Wrangler(
    "postgresql+psycopg2://taiga:Squeezing-Subprime9-Partake@taiga.murraycountymed.org:5432/taiga"
)
sql = pdw.read_sql_file("build/history.sql")
df = pdw.df_fetch(sql)
# df = pdw.df_fetch("select * from accounts", index_col="guid")
print(df.index.name)
print(df.index.dtype)
print(df.dtypes)
print(df)
"""


pdw = Pandas_DB_Wrangler("/home/justin/.config/joplin-desktop/database.sqlite")
# sql = pdw.read_sql_file("build/transactions_master.sql")

sql = pdw.read_sql_file("build/joplin.sql")
notes = pdw.df_fetch(sql)
print(pdw.options)
print(notes.dtypes)
