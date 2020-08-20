import mysql.connector
from types import SimpleNamespace
import json
from pathlib import Path


def tupleSplit(result, sliceList=None, splitChar=' '):
    if sliceList is None:
        prep = tuple(result.split(splitChar))
    else:
        prep = tuple([result.split(splitChar)[i] for i in sliceList])

    return prep


def insertIntoTable(record, user, password, host, db, table, cols):
    import mysql.connector
    # create connection string
    conn = mysql.connector.connect(user=user, password=password,
                                   host=host, database=db)

    # create cursor
    cnx = conn.cursor()

    # create insert statement
    insert_stmt = ("INSERT INTO " + table + cols +
                   "VALUES (%s, %s, %s, %s)")

    try:
        # insert statement for each item in df
        cnx.execute(insert_stmt, record)

        # print update to console
        # print(str(i + 1) + ' records written')

        # commit changes in the database
        conn.commit()

    except:

        # roll back in case of error
        cnx.rollback()
        raise Exception('unable to insert to %s' % table)

    # close connection to server
    cnx.close()


# testing
t = '2020-08-20 12:15:05 - Successful ping response example.com'
result = tupleSplit(result=t, sliceList=[0, 1, 3, 6])

with open(str(Path.home()) + '/.ssh/apiKeys') as f:
    apiItems = json.load(f)['logs']['hostPing']

# create simple namespace
argsL = SimpleNamespace(**apiItems)

# submit to table
insertIntoTable(record=result, user=argsL.user, password=argsL.password,
                host=argsL.host, db=argsL.database, table=argsL.table,
                cols=argsL.columns)
