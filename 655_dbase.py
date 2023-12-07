# Import approved military equipment sales data from Excel to SQLite database

import xlrd
import sqlite3

def make_db(dbname):
    """
    make_db: Creates a sqlite database for storing military sales data
    :param dbname: filename to use for database
    :rtype None:
    """
    mk_stmt = '''CREATE TABLE sales (country TEXT, 
                                     year INT, 
                                     articles INT, 
                                     services INT)'''
    curs = sqlite3.connect(dbname).cursor()
    curs.execute(mk_stmt)
    curs.connection.close()
    
def import_xl(dbname, fname, sheets):
    """
    import_xl: Loads military sales data from Excel sheet into database
    :param dbname: sqlite database filename
    :param fname: Excel spreadsheet filename
    :param years: list of sheet names to extract from
    :rtype None:
    """
    curs = sqlite3.connect(dbname).cursor()
    ins_stmt = 'INSERT INTO sales (country, year, articles, services) VALUES (?,?,?,?)'
    for sheet_name in sheets:
        rows = xlrd.open_workbook(fname).sheet_by_name(sheet_name).get_rows()
        # Skip column labels
        rows.next()
        adds = list()
        # Assume sheet is the year
        year = int(sheet_name)
        for row in rows:
            country = row[0].value.strip()
            articles = row[1].value
            if year in (2006, 2007, 2008):
                if row[4].ctype != 0:
                    # 2006-08
                    services = int(row[4].value)
                else:
                    # Empty cell = no services sold
                    services = 0
            elif row[2].ctype != 0:
                # 2010-12
                services = int(row[2].value)
            else:
                # Empty cell = no services sold
                services = 0
            adds += [[country, year, articles, services]]
        curs.executemany(ins_stmt, adds)
        adds = list()
    curs.connection.commit()
    curs.connection.close()
    
def rebuild():
    make_db('655.sqlite')
    import_xl('655.sqlite', 'rpt655.xls', ['2006', '2007', '2008', '2010', 
                                           '2011', '2012'])