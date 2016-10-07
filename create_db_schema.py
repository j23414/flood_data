import sqlite3

def drop_all_tables(cur, table_list):
    for table in table_list:
        cur.execute("DROP TABLE {}".format(table))

con = sqlite3.connect("floodData.sqlite")
c = con.cursor()

tables = ['variables', 'datavalues', 'sites']
drop_all_tables(c, tables)

c.execute("CREATE TABLE variables (VariableID INTEGER PRIMARY KEY AUTOINCREMENT , VariableName text, VariableType text, Units text);")
c.execute("CREATE TABLE datavalues (ValueID INTEGER PRIMARY KEY AUTOINCREMENT, Value real, Datetime text, VariableID, SiteID);")
c.execute("CREATE TABLE sites (SiteID INTEGER PRIMARY KEY AUTOINCREMENT, SiteName text, SiteCode text, Lat real, Lon real);")


con.commit()
con.close()
