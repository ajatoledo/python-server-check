#!/usr/bin/env python

# Updates applied - Alex Aguilar
from types import SimpleNamespace
import json
import os
import argparse
from customFunctions import tupleSplit, insertIntoTable


def main():
    parser = argparse.ArgumentParser(description='Output Processing')

    # read config items
    parser.add_argument('outputFile', help='output file to parse')
    parser.add_argument('-sp', '--splitChar', default=' ',
                        help='specify character to split statement')
    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help='verbose output response messages')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-sl', '--sliceList', required=True,
                               help='specify which statement items to pull')

    try:
        args = parser.parse_args()
        output = args.outputFile
        sliceList = [int(item) for item in args.sliceList.split(',')]
        splitChar = args.splitChar
        verbose = args.verbose

    except:
        parser.print_help()
        exit(-1)

    # read in config items - table, cols, etc.
    loc = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
    with open(loc) as f:
        serverPing = json.load(f)['mysql']

    # create simple namespace
    argsL = SimpleNamespace(**serverPing)

    with open(output) as fp:
        lines = [line.rstrip() for line in fp]

    if len(output) > 1:
        for i, out in enumerate(lines):
            # parse data, prep for loading
            result = tupleSplit(result=out, sliceList=sliceList,
                                splitChar=splitChar)

            # submit to table
            insertIntoTable(record=result, user=argsL.user,
                            password=argsL.password,
                            host=argsL.host, db=argsL.database,
                            table=argsL.table,
                            cols=argsL.columns)

            if verbose:
                if (i + 1) is 1:
                    print('Status update: 1 record written; last record '
                          'written for hostname: {0}'.format(result[-1]))
                else:
                    print('Status update: ' + str(
                        i + 1) + ' records written; last record '
                                 'written for hostname: {0}'.format(result[-1]))

    else:
        # parse data, prep for loading
        result = tupleSplit(result=lines, sliceList=sliceList,
                            splitChar=splitChar)

        # submit to table
        insertIntoTable(record=result, user=argsL.user, password=argsL.password,
                        host=argsL.host, db=argsL.database, table=argsL.table,
                        cols=argsL.columns)

        if verbose:
            print(
                'Status update: 1 record written; last record written for '
                'hostname: {0}'.format(result[-1]))


if __name__ == '__main__':
    main()
