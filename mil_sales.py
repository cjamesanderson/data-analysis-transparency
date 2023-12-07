# Functions for importing US Military Sales data into SQLite DB

import xlrd
import sqlite3

def make_db(dbname):
    """
    make_db: Creates a sqlite database for storing military sales data
    :param dbname: filename to use for database
    :rtype None:
    """
    mk_stmt = 'CREATE TABLE sales (country TEXT, region TEXT, year INT, sales INT)'
    curs = sqlite3.connect(dbname).cursor()
    curs.execute(mk_stmt)
    curs.connection.close()
    
def import_xl(dbname, fname):
    """
    import_xl: Loads military sales data from Excel sheet into database
    :param dbname: sqlite database filename
    :param fname: Excel spreadsheet filename
    :rtype None:
    """
    curs = sqlite3.connect(dbname).cursor()
    ins_stmt = 'INSERT INTO sales (country, region, year, sales) VALUES (?,?,?,?)'
    sheet_name = 'Foreign Military Sales 2005 to 2013'
    rows = xlrd.open_workbook(fname).sheet_by_name(sheet_name).get_rows()
    # Skip column labels
    rows.next()
    adds = list()
    region = None
    for row in rows:
        # CC column occupied == country data row
        if row[11].ctype != 0:
            country = row[0].value.strip()
            year = 2006
            # 2006-2013 data
            for cell in row[2:10]:
                # Cell not occupied by Unicode string (i.e. not empty)
                if cell.ctype != 1:
                    adds += [[country, region, year, int(cell.value)]]
                year += 1
            if len(adds) > 0:
                curs.executemany(ins_stmt, adds)
                adds = list()
        else:
            region = row[0].value.strip()
    curs.connection.commit()
    curs.connection.close()
                    
            