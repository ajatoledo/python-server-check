#!/usr/bin/env python

# Author of original email work - Mark Royer
# Updates applied - Alex Aguilar

import argparse
import os
import json
import time
import pytz
from datetime import datetime
from py.customFunctions import ping, pushoverRequest, sendMailPlain


def main():
    parser = argparse.ArgumentParser()

    # check for config file
    try:

        # read in config file
        loc = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
        with open(loc) as f:
            data = json.load(f)

        # reading default keys and user from config
        parser.add_argument('-t', '--token', default=data['pushover']['token'],
                            help='pushover application token')
        parser.add_argument('-u', '--user', default=data['pushover']['user'],
                            help='pushover user token')

    except:

        parser.print_help()
        exit(-1)

    # read config items
    parser.add_argument('host', help='host name to verify')
    parser.add_argument('-a', '--attempts', type=int, default=10,
                        help='max attempts')
    parser.add_argument('-w', '--wait', type=int, default=20,
                        help='wait time in seconds (default: 20)')
    parser.add_argument('-g', '--wget', action='store_true',
                        help='use wget instead of icmp ping')
    parser.add_argument('-v', '--verbose', type=bool, action='store_true',
                        help='verbose output response messages')
    parser.add_argument('-ts', '--timestamp', type=bool, action='store_true',
                        help='append timestamp to output, useful for logging')

    try:
        args = parser.parse_args()
        hostname = args.host
        token = args.token
        user = args.user
        maxAttempts = args.attempts
        waitTime = args.wait  # seconds
        useWget = args.wget
        verbose = args.verbose
        timestamp = args.timestamp

    except:
        parser.print_help()
        exit(-1)

    # capture timezone if ts passed
    if timestamp:
        try:
            timezone = pytz.timezone(data['timestamp']['timezone'])
        except:
            print('timezone information not provided in config file')
            exit(-1)

    response = ping(hostname=hostname, useWget=useWget, verbose=verbose)
    attempts = 1

    while response != 0 and attempts < maxAttempts:
        if verbose:
            if timestamp:
                print(
                    '%s Attempt %d to ping host %s failed. '
                    'Trying again in %d seconds.' % (
                        datetime.now(timezone).strftime(
                            "%Y-%m-%d %H:%M:%S") + ' -', attempts, hostname,
                        waitTime))
            else:
                print(
                    'Attempt %d to ping host %s failed. '
                    'Trying again in %d seconds.' % (
                        attempts, hostname, waitTime))

        time.sleep(waitTime)
        response = ping(hostname=hostname, useWget=useWget, verbose=verbose)
        attempts += 1

    if response != 0:
        if verbose:
            if timestamp:
                print(
                    '%s Attempt %d to ping host %s failed. '
                    'Giving up and sending pushover alert.' % (
                        datetime.now(timezone).strftime(
                            "%Y-%m-%d %H:%M:%S") + ' -', attempts, hostname))
            else:
                print(
                    'Attempt %d to ping host %s failed. '
                    'Giving up and sending pushover alert.' % (
                        attempts, hostname))

        # message that will be passed to pushover alert
        msg = ('%s failed to respond after %d ping attempts. '
               'Someone should probably investigate.' % (
                   hostname, attempts))

        pushoverRequest(token=token,
                        user=user,
                        message=msg)

        if timestamp:
            print('%s Failed to ping %s' % (
                datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S") + ' -',
                hostname))
        else:
            print('Failed to ping %s' % hostname)
    else:
        if timestamp:
            print('%s Successful ping response %s' %
                  (datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S") + ' -',
                   hostname))
        else:
            print('Successful ping response %s' % hostname)


if __name__ == '__main__':
    main()
