#!/usr/bin/env python

# Author of original email work - Mark Royer
# Updates applied - Alex Aguilar

import argparse
import os
import json
from types import SimpleNamespace
import time
import pytz
from datetime import datetime
from customFunctions import ping, pushoverRequest, sendMailPlain


def main():
    # create parser object
    parser = argparse.ArgumentParser()

    # check for config file
    try:

        # read in config items - table, cols, etc.
        loc = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
        with open(loc) as f:
            serverPing = json.load(f)

        # create simple namespace
        argsL = SimpleNamespace(**serverPing)

    except:
        parser.print_help()
        raise Exception(
            'Config.json not found; confirm it has been created.\n'
            'Run configSetup.py if config.json hasn\'t been created')

    # read config items
    parser.add_argument('host', type=str, help='host name to verify')
    parser.add_argument('-em', '--email', action='store_true',
                        help='if passed, sends e-mail using '
                             'config file credentials')
    parser.add_argument('-po', '--pushover', action='store_true',
                        help='if passed, sends pushover request using '
                             'config file credentials')
    parser.add_argument('-a', '--attempts', type=int, default=10,
                        help='max attempts')
    parser.add_argument('-w', '--wait', type=int, default=20,
                        help='wait time in seconds (default: 20)')
    parser.add_argument('-g', '--wget', action='store_true',
                        help='use wget instead of icmp ping')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose output response messages')
    parser.add_argument('-ts', '--timestamp', action='store_true',
                        help='append timestamp to output, useful for logging')

    try:
        args = parser.parse_args()
        hostname = args.host
        maxAttempts = args.attempts
        waitTime = args.wait  # seconds
        useWget = args.wget
        verbose = args.verbose
        email = args.email
        pushover = args.pushover
        timestamp = args.timestamp

    except:
        parser.print_help()
        exit(-1)

    # capture timezone if it's passed
    if timestamp:
        try:
            timezone = pytz.timezone(argsL.timestamp['timezone'])
        except:
            raise Exception(
                'timezone not found, confirm it has been '
                'configured in config.json.')

    # ping hostname
    response = ping(hostname=hostname, useWget=useWget, verbose=verbose)

    # create counter for while loop
    attempts = 1

    # if initial ping is unsuccessful, begin while loop and increment until max
    while response != 0 and attempts < maxAttempts:
        if verbose:
            if timestamp:
                print(
                    '{0} Attempt {1} to ping host {2} failed. '
                    'Trying again in {3} seconds.' .format(
                        datetime.now(timezone).strftime(
                            "%Y-%m-%d %H:%M:%S") + ' -', attempts, hostname,
                        waitTime))
            else:
                print(
                    'Attempt {0} to ping host {1} failed. '
                    'Trying again in {2} seconds.' .format(
                        attempts, hostname, waitTime))

        # sleep script before attempting ping again
        time.sleep(waitTime)

        # attempt ping again
        response = ping(hostname=hostname, useWget=useWget, verbose=verbose)

        # increment attempt count by 1
        attempts += 1

    # if while loop breaks, proceed to notification
    if response != 0:
        if verbose:
            if timestamp:
                print('{0} Attempt {1} to ping host {2} failed. '
                      'Giving up and sending notification.'
                      .format(
                        datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
                        + ' -', attempts, hostname))
            else:
                print(
                    'Attempt {0} to ping host {1} failed. '
                    'Giving up and sending notification.'.format(
                        attempts, hostname))

        # message that will be passed to notification
        msg = ('{0} failed to respond after {1} ping attempts. '
               'Someone should probably investigate.'
               .format(hostname, attempts))

        # determine which type of notifications should be sent
        if pushover:
            pushoverRequest(token=argsL.pushover['token'],
                            user=argsL.pushover['user'],
                            message=msg)

        if email:
            subject = ('{0} not responding' .format(hostname))
            sendMailPlain(mailSender=argsL.email['sender'],
                          mailPassword=argsL.email['password'],
                          receiver=[argsL.email['receiver']], message=msg,
                          smtpServer=argsL.email['smtpServer'],
                          port=argsL.email['smtpPort'], subject=subject)

        if timestamp:
            print('{0} Failed to ping {1}'.format(
                datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S") + ' -',
                hostname))
        else:
            print('Failed to ping {0}'.format(hostname))
    else:
        if timestamp:
            print('{0} Successful ping response {1}'.format(
                datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S") + ' -',
                hostname))
        else:
            print('Successful ping response {0}'.format(hostname))


if __name__ == '__main__':
    main()
