
import sys
import pandas
import pysqlite3
from warnings import filterwarnings


filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')
db_file = 'Ashish.db'

con = pysqlite3.connect(db_file)


cur = con.cursor()


def Ovrly():


    df1 = pandas.read_table("Overlay_2.dat",sep= "¶", quotechar="þ",engine='python',encoding="utf-8")
    df1.to_sql("Overlay_Table", con, if_exists='replace', index=False)

    clm4 = input("Identifier column in Target File\n")
    clm5 = input("Identifier column in overlay File\n")
    cml6 = input("Column name to update\n")
    clm7 = input("Column Where need to pull data\n")

    #query = "UPDATE Working_Table Set Units =(SELECT Units FROM Overlay_Table WHERE OVERLAY_Table.ID = Working_Table.ID) WHERE EXISTS(SELECT Units FROM Overlay_Table WHERE OVERLAY_Table.ID = Working_Table.ID)"
    query = "UPDATE Working_Table Set "+ cml6 +"=(SELECT "+ clm7 +" FROM Overlay_Table WHERE OVERLAY_Table."+ clm5 +" = Working_Table."+ clm4 +") WHERE EXISTS(SELECT "+ clm7 +" FROM Overlay_Table WHERE OVERLAY_Table."+ clm5 +" = Working_Table."+ clm4 +")"
    con.execute(query)

    con.commit()
    print("Overlay complete")

Ovrly()
#Not Working Query#######Need to check#
##UPDATE Working_Table SET ID = Overlay_Table.ID FROM Working_Table INNER JOIN Overlay_Table on Overlay_Table.Units = Working_Table.Units;


con.close()