#!/usr/bin/env python

# Author - Mark Royer

import argparse
import os
import sys
import json
import time
import http.client
import urllib

def ping(hostname, useWget):
    print('Attempting to ping host %s...' % hostname)
    if useWget:
        # This option is if icmp is blocked
        return os.system('wget -nv -O - ' + hostname  + ' > /dev/null 2>&1')
    else:
        # Send one packet and wait up to 10 seconds for a response
        return os.system('ping -c 1 -W 10 ' + hostname  + ' > /dev/null')


def main():

    # read in config file
    with open(os.path.join(sys.path[0], 'config')) as f:
        data = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host name to verify')
    parser.add_argument('-t', '--token', default=data['pushover']['token'], help='pushover application token')
    parser.add_argument('-u', '--user', default=data['pushover']['user'], help='pushover user token')
    parser.add_argument('-a', '--attempts', type=int, default=10, help='max attempts')
    parser.add_argument('-w', '--wait', type=int, default=20, help='wait time in seconds (default: 20)')
    parser.add_argument('-g', '--wget', action='store_true', help='use wget instead of icmp ping')

    try:
        args = parser.parse_args()

        hostname = args.host
        token = args.token
        user = args.user
        maxAttempts = args.attempts
        waitTime = args.wait # seconds
        useWget = args.wget
        
    except:
        parser.print_help()
        exit(-1)

    response = ping(hostname, useWget)
    attempts = 1

    while response != 0 and attempts < maxAttempts:
        print('Attempt %d to ping host %s failed. Trying again in %d seconds.' % (attempts, hostname, waitTime))
        time.sleep(waitTime)
        response = ping(hostname, useWget)
        attempts+=1

    if response != 0:
        print('Attempt %d to ping host %s failed. Giving up and sending pushover alert.' % (attempts, hostname))
        msg = '%s failed to respond after %d ping attempts. Someone should probably investigate.' % (hostname, attempts)
        
        conn = http.client.HTTPSConnection('api.pushover.net:443')
        conn.request('POST', '/1/messages.json',
            urllib.parse.urlencode({
                'token': token,
                'user': user,
                'message': msg,
            }), { 'Content-type': 'application/x-www-form-urlencoded' })
        conn.getresponse()

        # print 'Failed to ping %s.  Sent email to %s.' % (hostname, receivers)
        print('Failed to ping %s. Sent pushover alert.' % (hostname))

    else:
        print('Successful ping response from %s.  It\'s alive!' % (hostname))

if __name__ == '__main__':
    main()
