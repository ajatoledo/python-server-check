#!/usr/bin/env python

# Updates applied - Alex Aguilar
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
            lines = [line.rstrip() for line in fp]

        # replace new line string
        # lines = [sub.replace('\n', '') for sub in lines]

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


def pushoverRequest(token,
                    user,
                    message=None,
                    attachment=None,
                    device=None,
                    title=None,
                    url=None,
                    url_title=None,
                    priority=None,
                    sound=None,
                    timestamp=None, verbose=False):
    import requests

    # capture input arguments as dict
    pushover_args = {
        'token': token,
        'user': user,
        'message': message,
        'attachment': attachment,
        'device': device,
        'title': title,
        'url': url,
        'url_title': url_title,
        'priority': priority,
        'sound': sound,
        'timestamp': timestamp
    }

    # create updated dict to include non-None items
    pushover_args = {k: v for k, v in pushover_args.items() if v is not None}

    # create post url
    urlPush = requests.post(
        'https://api.pushover.net/1/messages.json',
        data=pushover_args,
        headers={'User-Agent': 'Python'})

    # raise exception if response was not successful
    if urlPush.status_code == 200:

        if verbose:
            print(
                'Pushover returned OK status, check your device '
                'for a pushover notification; if you do not see '
                'a notification, check the pushover application settings.')

            # return post response
            return urlPush

    if urlPush.status_code != 200:
        raise Exception(
            'Pushover response status was: {0}, indicating the pushover '
            'request was not successful.'.format(urlPush.status_code))


def sendMailPlain(mailSender, mailPassword, receiver: list, message: str,
                  smtpServer: str = 'smtp.gmail.com',
                  port: int = 465, subject=None, verbose: bool = False):
    import smtplib
    import ssl
    from email.mime.text import MIMEText
    if subject is None:
        subject = 'no subject specified'
    else:
        pass

    # sends a plain text message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = mailSender
    msg['To'] = ', '.join(receiver)

    # create a secure SSL context
    context = ssl.create_default_context()

    # try submitting email, if not successful, print to console
    try:
        with smtplib.SMTP_SSL(smtpServer, port,
                              context=context) as server:
            server.login(mailSender, mailPassword)
            server.sendmail(mailSender, receiver, msg.as_string())

            # output result if verbose is set
            if verbose:

                if len(receiver) > 1:
                    print('E-mails sent to {0}.'.format(', '.join(receiver)))

                else:
                    print('E-mail sent to {0}.'.format(', '.join(receiver)))

    except:
        # output result if verbose is set
        if verbose:
            if len(receiver) > 1:
                print('E-mails not sent to {0}.'.format(', '.join(receiver)))
            else:
                print('E-mail not sent to {0}.'.format(', '.join(receiver)))


def ping(hostname: str, useWget: bool = False, verbose: bool = False):
    import os

    if verbose:
        print('Attempting to ping host {0}...'.format(hostname))

    if useWget:
        # This option is if icmp is blocked
        return os.system('wget -nv -O - ' + hostname + ' > /dev/null 2>&1')
    else:
        # Send one packet and wait up to 10 seconds for a response
        return os.system('ping -c 1 -W 10 ' + hostname + ' > /dev/null 2>&1')
