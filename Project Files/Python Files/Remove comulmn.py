import pandas
import pysqlite3

db_file = 'Ashish.dat.db'

con = pysqlite3.connect(db_file)


cur = con.cursor()



def rmv_clmn():

    #clm_name3 = str(input('Add column name to delete\n'))
    query = "ALTER TABLE Working_Table DROP COLUMN Year"
    con.execute(query)

    con.commit() 

rmv_clmn()

con.close()