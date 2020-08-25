#!/usr/bin/env python

import json
import pytz
import os
from customFunctions import setupLoop, sendMailPlain, pushoverRequest


def main():
    # determining which config items will be setup

    # timezone
    timeZoneSetup = setupLoop(
        questionText='Do you want to specify a timezone for local '
                     'reporting? By default UTC will be used.')

    if timeZoneSetup == 'Y':

        # timestamp setup
        timezone = input('Enter timezone (TZ code) to be used; '
                         'if blank, UTC will be used: ')

        # if blank, set to utc
        if timezone is '':
            timezone = 'UTC'

        # validate input tz code
        if timezone in pytz.all_timezones:
            pass
        else:
            raise ValueError(
                'Invalid timezone string. Review timezone string settings and '
                'restart setup process.')

        # compile timezone to dict
        timestamp = {'timezone': timezone}

    elif timeZoneSetup == 'N':
        print('Timezone not set, as a result timestamps will use UTC; if '
              'you would like to setup a timezone, re-run configSetup.py.')

        # set timezone to UTC
        timezone = 'UTC'

        # save timestamp to specified timezone
        timestamp = {'timezone': timezone}

    # email
    emailSetup = setupLoop(
        questionText='Will you be setting up an e-mail account?')

    if emailSetup == 'Y':
        sender = input('Enter email account that will be '
                       'used to send messages: ')
        password = input('Enter email account password; '
                         'note stored in plaintext: ')
        receiver = input('Enter email address(es) that should be notified; \n'
                         'enter multiple addresses as comma-delimited, '
                         'e.g. p1@example.com, p2@example.com: ')

        # remove space if needed
        receiver = receiver.replace(' ', '')

        # the following items can be left blank for default
        smtpServer = input('Enter smtpserver address; '
                           'if blank smtp.gmail.com will be used: ')

        # fill in blank response
        if smtpServer == '':
            smtpServer = 'smtp.gmail.com'

        port = input('Enter email server port; if blank, 465 will be used: ')

        # fill in blank response
        if port == '':
            port = 465

        # compile email items into a dict
        email = {'sender': sender, 'password': password, 'receiver': receiver,
                 'smtpServer': smtpServer, 'port': port}

        # ask user if they would like to test email
        testEmail = setupLoop(questionText='Would you like to test email '
                                           'using provided arguments?')

        if testEmail == 'Y':
            print('Running email test...')
            test = email.copy()
            test.update({'message': 'Woo-hoo! Email setup was successful!'})

            # send test email message
            sendMailPlain(mailSender=test['sender'],
                          mailPassword=test['password'],
                          receiver=[test['receiver']], message=test['message'],
                          smtpServer=test['smtpServer'], port=int(test['port']),
                          subject=test['subject'], verbose=True)

        else:
            print(
                'Email test was not conducted; if you answered N by accident, '
                're-run the setup process. Otherwise, please be sure '
                'that your email information is setup properly.')

    elif emailSetup == 'N':
        print('Email not set, as a result email notifications cannot be used; '
              'if you would like to setup email, re-run configSetup.py.')
        email = None

    # pushover
    pushoverSetup = setupLoop(
        questionText='Will you be setting up a pushover account?')

    if pushoverSetup == 'Y':

        # pushover setup
        token = input('Enter pushover application api token: ')
        user = input('Enter pushover user or group key: ')

        # ask user if they want to additional pushover arguments in notification
        pushoverAdvanced = setupLoop(questionText='Would you like to enter '
                                                  'additional pushover '
                                                  'arguments, e.g., '
                                                  'notification title, '
                                                  'link, etc.? ')

        if pushoverAdvanced == 'Y':
            attachment = input('Enter pushover application attachment: ')
            device = input('Enter device name: ')
            title = input('Enter pushover application attachment: ')
            url = input('Enter url: ')
            url_title = input('Enter url_title: ')
            priority = input('Enter notification priority: ')
            sound = input('Enter pushover sound to use in notification: ')

            # compile pushover with additional arguments to dict
            pushover = {'token': token, 'user': user, 'attachment': attachment,
                        'device': device, 'title': title, 'url': url,
                        'url_title': url_title, 'priority': priority,
                        'sound': sound}

        if pushoverAdvanced == 'N':
            # compile pushover items without additional arguments to dict
            pushover = {'token': token, 'user': user}

        testPO = setupLoop(questionText='Would you like to test pushover?')

        if testPO == 'Y':
            print('Running pushover test...')
            test = pushover.copy()
            test.update({'message': 'Woo-hoo! Pushover setup was successful!'})

            out = pushoverRequest(token=test['token'],
                                  user=test['user'],
                                  message=test['message'], verbose=True)

        else:
            print('Pushover test was not conducted; if you answered N by '
                  'accident, re-run the setup process. Otherwise, please '
                  'be sure that your pushover application is setup properly.')

    # if user select to input mysql connection information, prompt them to
    # input information and then create config

    elif pushoverSetup == 'N':
        print('Pushover not set, as a result pushover notifications cannot '
              'be used; if you would like to setup pushover, '
              're-run configSetup.py.')

        pushover = None

    mysqlSetup = setupLoop(
        questionText='Will you be setting up a mysql connection?')

    if mysqlSetup == 'Y':

        # "mysql":
        user = input('Enter mysql username: ')
        password = input('Enter mysql password; note stored in plaintext: ')
        host = input('Enter mysql hostname: ')
        database = input('Enter mysql database (schema): ')
        table = input('Enter mysql table to which values will be written: ')
        columns = input(
            'Enter columns that will be updated in specified table; delimit '
            'column names with commas: ')

        # compile mysql items to dict
        mysql = {'user': user, 'password': password, 'host': host,
                 'database': database,
                 'table': table, 'columns': columns}

    # if user selected to not include mysql, create config
    elif mysqlSetup == 'N':
        mysql = None

    # create config json
    config = {'timestamp': timestamp, 'email': email, 'pushover': pushover,
              'mysql': mysql}

    # keep only the items for which information was provided
    config = {k: v for k, v in config.items() if v is not None}

    # print config for confirmation:
    configPreview = setupLoop(
        questionText='Preview the config file to be created?')

    if configPreview == 'Y':
        print(json.dumps(config, indent=2))

    # print config for confirmation:
    writeConfig = setupLoop(
        questionText='Should the config file be written to file?')

    if writeConfig == 'Y':

        # create file path to write file in current directory
        loc = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

        # write config file to disk
        with open(loc, 'w') as f:
            json.dump(config, f)

    # raise an issue if config is not saved
    elif writeConfig == 'N':
        raise Exception('Config file not written to file.')


if __name__ == '__main__':
    main()
