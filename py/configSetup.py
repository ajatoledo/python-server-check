#!/usr/bin/env python

import json
import requests
import pytz


def main():
    while True:
        setup_select = input('Will you be setting up a mysql connection? Y/N')
        if 1 <= len(setup_select) < 4:
            if setup_select[0].upper() in ['Y', 'N']:
                # prep selection value for case
                setup_select = setup_select[0].upper()
                break
            print(
                'Please indicate Y/N; received input {0}'.format(setup_select))

    # pushover setup
    token = input('Enter pushover application api token: ')
    user = input('Enter pushover user key: ')
    pushover = {'token': token, 'user': user}

    testPO = input('Would you like to test pushover? Y/N')
    if testPO[0].upper() == 'Y':
        print('Running pushover test...')
        test = pushover.copy()
        test.update({'message': 'Woo-hoo! Pushover setup was successful!'})

        out = requests.post('https://api.pushover.net/1/messages.json',
                            data=test,
                            headers={'User-Agent': 'Python'})

        if out.status_code != 200:
            print('')
            raise Exception(
                'Pushover response status was: {0}, indicating the pushover '
                'request was not successful; exiting setup now. \nReview pushover '
                'settings and restart setup process.'.format(
                    out.status_code))
        else:
            print(
                'Pushover returned OK status, check your device for a pushover '
                'notification; if you don\'t see a notification, check the pushover'
                'application settings and re-run setup if needed..')

    else:
        print('Pushover test was not conducted; if you answered N by accident, '
              're-run the setup process. Otherwise, please be sure '
              'that your pushover application is setup properly.')

    # timestamp setup
    timezone = input('Enter timezone to be used; use TZ code: ')
    timestamp = {'timezone': timezone}

    if timezone in pytz.all_timezones:
        pass
    else:
        raise ValueError(
            'Invalid timezone string. Review timezone string settings and '
            'restart setup process.')

    # if user select to input mysql connection information, prompt them to
    # input information and then create config
    if setup_select == 'Y':

        # "mysql":
        user = input('Enter mysql username: ')
        password = input('Enter mysql password; note stored in plaintext: ')
        host = input('Enter mysql hostname: ')
        database = input('Enter mysql database (schema): ')
        table = input('Enter mysql table to which values will be written: ')
        columns = input(
            'Enter columns that will be updated in specified table; delimit '
            'column names with commas: ')
        mysql = {'user': user, 'password': password, 'host': host,
                 'database': database,
                 'table': table, 'columns': columns}

        # create config json
        config = {'pushover': pushover, 'timestamp': timestamp, 'mysql': mysql}

    # if user selected to not include mysql, create config
    elif setup_select == 'N':
        config = {'pushover': pushover, 'timestamp': timestamp}

    # write config file to disk
    with open('py/config.json', 'w') as f:
        json.dump(config, f)


if __name__ == '__main__':
    main()
