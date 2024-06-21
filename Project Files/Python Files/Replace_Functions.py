import pandas
import sqlite3

db_file = 'Ashish.dat.db'

con = sqlite3.connect(db_file)


cur = con.cursor()
#-------------table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

####To view  column names #####
#--------------for row in cur.execute('SELECT * FROM sqlite_master;'):
#--------------    print(row)
#------------------print(table_list)






#########To Update a Single Value############
#def update(clm_name):
    #new_value = str(input('Add updated value\n'))
    #doc_id = str(input('Add Document ID\n'))

    #con.execute("UPDATE Working_Table SET " + clm_name + "=(?) WHERE ID = (?)",(new_value, doc_id,))
    #con.commit() 

#update(input("Add colum name to update\n"))

#########To Update Whole Column############
def update_clm(clm_name):                                          ####Update function with intial parameter for target column name
    new_value = str(input('Add updated value\n'))                ####Input for updated value

    con.execute("UPDATE Working_Table SET " + clm_name + "=(?)",(new_value,))           ####Query for mass replace, ###(new_value,))---IN THIS EXTRA COMMA AT THE END IS UNPACKING OF TUPLE
    con.commit()                                                                        ####execution

update_clm(input("Add colum name to update\n"))                                             ####call to function


#########To Update a Single Value############
def update_val(clm_name2):    
    old_value = str(input('Add Old Value\n'))
    new_value = str(input('Add new Value\n'))

    con.execute("UPDATE Working_Table SET " + clm_name2 + "=(?) WHERE " + clm_name2 + "=(?)",(new_value, old_value,))
    con.commit() 

update_val(input("Add colum name to update\n"))


'''
Not is use for now, Unable to test with data yet

#################Removing white spaces################
def rmv_whitspce(clm_name3):

    con.execute("UPDATE Working_Table SET " + clm_name3 + "=Trim(" + clm_name3 + ")")
    con.commit() 

rmv_whitspce(input("Add colum name to update\n"))
'''

con.close()