import sqlite3

def drop_all_tables(cur, table_list):
    for table in table_list:
        try:
            cur.execute("DROP TABLE {}".format(table))
        except sqlite3.OperationalError:
            pass

con = sqlite3.connect("floodData.sqlite")
c = con.cursor()

tables = ['variables', 'datavalues', 'sites']
drop_all_tables(c, tables)

c.execute("""CREATE TABLE variables\
            (VariableID INTEGER PRIMARY KEY AUTOINCREMENT, \
            VariableCode text, \
            VariableName text, \
            VariableType text, \
            Units text);""")
c.execute("""CREATE TABLE sites \
            (SiteID INTEGER PRIMARY KEY AUTOINCREMENT, \
            SiteCode text, \
            SiteName text, \
            SourceOrg text, \
            Lat real, \
            Lon real);""")
c.execute("""CREATE TABLE datavalues \
            (ValueID INTEGER PRIMARY KEY AUTOINCREMENT, \
            Value real, \
            Datetime text, \
            VariableID, \
            SiteID,\
            FOREIGN KEY(VariableID) REFERENCES variables(VariableID),\
            FOREIGN KEY(SiteID) REFERENCES sites(SiteID)\
            );""")



con.commit()
con.close()
