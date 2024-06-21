import pandas as pd
import sqlite3
import csv
import chardet
import numpy as np

db_file = 'Ashish.dat.db'

conn = sqlite3.connect(db_file)




cursor = conn.cursor()


db_df = pd.read_sql(sql="SELECT * FROM Working_Table",con=conn)
db_df.to_csv('database.dat',sep= "¶",quoting=csv.QUOTE_ALL,quotechar="þ",encoding="utf-8",index=False)

conn.close()