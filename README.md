# python-server-check

A simple Python script to see if a server is still alive. If the
server does not respond after a specified number of attempts (default: 10), the script will email
recipients indicated in the script.

## Updated to Use Pushover

## Requirements

<!-- The `python-server-check` program requires Python and *some* email daemon is installed.  On Debian-based systems, [Exim4](https://wiki.debian.org/Exim) is a reasonable choice.  It can be installed and configured using the following commands.

```
sudo apt-get install exim4
sudo dpkg-reconfigure exim4-config
```
 -->

The `python-server-check` program requires Python and a pre-configured [Pushover](https://pushover.net) application with user and application token.  

## Building

<!-- No need to build anything.  However, you will want to modify the
script to send email to the appropriate people.  After modifications,
just run using the Python interpreter. -->

No need to build anything.  However, you will want to modify the
script to read to a config file, or alternatively input user and app tokens each time the script is run.  After modifications,
just run using the Python interpreter.

## Basic Usage

The script can be executed in the following manner.

```
usage: checkServer.py [-h] [-a ATTEMPTS] [-w WAIT] [-g]
                      host sender [recipients [recipients ...]]

positional arguments:
  host                      host name to verify

optional arguments:
  -t, --token           pushover application token; needed for pushover alerts
  -u, --user            pushover user token; needed for pushover alerts
  -h, --help            show this help message and exit
  -a ATTEMPTS, --attempts ATTEMPTS
                        max attempts
  -w WAIT, --wait WAIT  wait time in seconds (default: 20)
  -g, --wget            use wget instead of icmp ping
  -v, --verbose         if provided, process is verbose as it pings
```

As an example, invoking the script as

```bash
./checkServer.py foo.com -t app_token -u user_token
```

checks to see if `foo.com` reachable by ping.  If `foo.com` is not
reachable, a call to the specified Pushover app is made.

Using the `--wget` option allows you to specify an alternative port if
icmp traffic is blocked or ignored.  Specify the port by appending it
to the host name.  For example, specify `foo.com:8080` would use wget
to check for the default page served on port **8080**.

## Config Setting
If you want the script to read a pre-configured config file, create a file called `config` using the supplied `config_example.json` and place it into the same directory ad the python script. Using this allows you to omit application and user token when running the script.

## Using Cron

If you are using this script, then you probably want to use it with cron.

Typing

```
crontab -e
```

at a terminal will allow you to edit the local user's cron job file.

Adding a line such as

```
*/30 * * * * ~/checkServer.py -t app_token -u user_token
```

will check every 30 minutes that the server is still accessible.  This
assumes that the `checkServer.py` is placed in your home directory and
is executable.

## License

The project is licensed under the terms of the
[GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.
