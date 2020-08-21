#!/usr/bin/env python

# Updates applied - Alex Aguilar
from types import SimpleNamespace
import json
from pathlib import Path
from customFunctions import logCleaning, insertIntoTable

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

# loop through and create insert statement for each item in df
for i, row in records.iterrows():

    # submit to table
    insertIntoTable(record=tuple(row), user=argsL.user, password=argsL.password,
                    host=argsL.host, db=argsL.database, table=argsL.table,
                    cols=argsL.columns)

    # print update to console
    if (i + 1) is 1:
        print('Status update: 1 record written; last record '
              'written for hostname: {0}'.format(tuple(row)[-1]))
    else:
        print('Status update: ' + str(
            i + 1) + ' records written; last record '
                     'written for hostname: {0}'.format(tuple(row)[-1]))
