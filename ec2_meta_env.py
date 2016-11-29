#!/usr/bin/env python
"""A simple package to manifest EC2 instance metadata as environment variables.

Copyright (C) 2016  Tobias McNulty

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""
import argparse
import os
import subprocess
import sys

import requests

version = "0.1.0"


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e',
        '--env',
        action='append',
        help='an EC2 meta key to add as an environment variable, e.g., "local-ipv4" or '
             '"public-keys/0/openssh-key". The environment variable name will be created by '
             'prepending the name with "EC2_", uppercasing, and replacing all forward slashes and '
             'dashes with underscores, e.g., "EC2_LOCAL_IPV4" or "EC2_PUBLIC_KEYS_0_OPENSSH_KEY"',
    )
    parser.add_argument(
        '--override',
        action='store_true',
        help='if set, override existing environment variables of the same name',
    )
    parser.add_argument(
        '-s',
        '--strict',
        action='store_true',
        help='if set, fail immediately if EC2 metadata cannot be retrieved',
    )
    parser.add_argument(
        '-t',
        '--timeout',
        default=0.2,
        help='modify the HTTP request timeout (the default is 200 ms)',
    )
    parser.add_argument(
        'command',
        nargs='+',
        help='the shell command to run with the specified environment variables',
    )
    return parser.parse_args(args)


def get_environ(base_env, args):
    base_url = 'http://169.254.169.254/latest/meta-data/'
    # need to start with existing base_env so setdefault() works as intended
    environ = base_env.copy()
    for key in args.env or []:
        env_name = 'EC2_' + key.replace('/', '__').replace('-', '_').upper()
        try:
            value = requests.get(base_url + key, timeout=args.timeout).text
        except requests.exceptions.RequestException:
            if args.strict:
                raise
            value = None
        if value:
            if args.override:
                environ[env_name] = value
            elif value:
                environ.setdefault(env_name, value)
    return environ


def run_cmd(cmd, environ):
    process = subprocess.Popen(cmd, env=environ)
    process.wait()
    return process.returncode


def main(base_env=os.environ, args=sys.argv[1:]):
    args = parse_args(args)
    env = get_environ(base_env, args)
    return run_cmd(args.command, env)


if __name__ == "__main__":
    # execute only if run as a script
    main()
