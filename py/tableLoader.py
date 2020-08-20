import mysql.connector
from types import SimpleNamespace
import json
from pathlib import Path


def logCleaning(file, replaceChar=' ', colIndex=None, colNames=None):
    # import libraries needed below
    import pandas as pd
    from pathlib import Path

    # evaluate whether file exists
    try:
        # check whether provided path exists
        Path(file).exists()

        # if passes, then open file
        with open(file) as fp:
            lines = fp.readlines()

        # replace new line string
        lines = [sub.replace('\n', '') for sub in lines]

        # convert lines to df
        df = pd.DataFrame(lines)

        # split string by provided character
        df = df[0].str.split(replaceChar, expand=True)

        # determine whether a subset of columns should be kept based on index
        if colIndex is None:
            pass
        else:
            df = df[df.columns[colIndex]]

        # if name list provided; apply names to columns
        if colNames is None:
            pass
        else:
            df.columns = colNames

    # raise error if file not found
    except:
        raise Exception('%s not found' % file)

    return df


# prepare data for upload
records = logCleaning(file=str(Path.home()) + '/host_output.log',
                      colIndex=[0, 1, 3, 6],
                      colNames=['DATE', 'TIME', 'RESPONSE', 'HOST'])

# prepare database connection
# read in the arguments needed for connection
with open(str(Path.home()) + '/.ssh/apiKeys') as f:
    apiItems = json.load(f)['logs']['hostPing']

# create simple namespace
argsL = SimpleNamespace(**apiItems)

# create connection string
conn = mysql.connector.connect(user=argsL.user, password=argsL.password,
                               host=argsL.host, database=argsL.database)

# create cursor
cnx = conn.cursor()

# create insert statement
insert_stmt = ("INSERT INTO " + argsL.table + argsL.columns +
               "VALUES (%s, %s, %s, %s) ")

try:
    # loop through and create insert statement for each item in df
    for i, row in records.iterrows():
        cnx.execute(insert_stmt, tuple(row))

        # print update to console
        print(str(i + 1) + ' records written')

    # commit changes in the database
    conn.commit()

except:

    # roll back in case of error
    cnx.rollback()
    raise Exception('unable to insert to %s' % argsL.table)

# close connection to server
cnx.close()
