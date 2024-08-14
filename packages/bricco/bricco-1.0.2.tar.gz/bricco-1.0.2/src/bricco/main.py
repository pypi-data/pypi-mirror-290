'''
Bricco is a Tor bridges testing tool.

Details: https://pypi.org/project/bricco
Git repo: https://codeberg.org/screwery/bricco
'''

__version__ = '1.0.2'
__repository__ = 'https://codeberg.org/screwery/bricco'
__bugtracker__ = 'https://codeberg.org/screwery/bricco/issues'

import re
import subprocess as sp
import logging
import socket
import sys
from contextlib import closing
from argparse import ArgumentParser, RawDescriptionHelpFormatter

TIMEOUT_DEFAULT = 5 # sec

OBFS4_BRIDGE_REGEXP = re.compile(
    r'(obfs4\s+' +
    r'(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d{1,5})\s+' +
    r'[0-9A-F]{40}\s+' +
    r'cert=[A-Za-z0-9\+\/]{70}\s+' +
    r'iat-mode=[012])'
    )

VANILLA_BRIDGE_REGEXP = re.compile(
    r'((?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d{1,5})\s+' +
    r'[0-9A-F]{40})'
    )

BFAIL_MSG = '\033[0;31mBridge at %s:%s is unavailable [%s]\033[0m'
BSUCCESS_MSG = '\033[0;32m\033[1mBridge at %s:%s is available!\033[0m'
TEST_HELP = 'Find bridges in some text file, test them, and save available bridges'
SOCKET_TIMEOUT_HELP = (f'Socket timeout in sec [default: {TIMEOUT_DEFAULT}]. ' +
                       'Ignored if nmap in use')
NMAP_HELP = ('Nmap executable to use instead of Python3 socket. ' +
             'Presumably is faster and more accurate [default: None]')

## ------======| TEST COMMAND |======------

def bricco_test(input_file, output_file, socket_timeout, nmap_exec):
    if nmap_exec is not None:
        result = sp.run([nmap_exec, '--help'], stdout=sp.DEVNULL)
        if result.returncode != 0:
            raise RuntimeError('Nmap executable is absent or damaged!')
    with open(input_file, 'rt') as fi:
        data = fi.read()
    checked = []
    with open(output_file, 'wt') as fo:
        found_bridges = []
        found_bridges.extend(OBFS4_BRIDGE_REGEXP.findall(data))
        found_bridges.extend(VANILLA_BRIDGE_REGEXP.findall(data))
        for item in found_bridges:
            if f'{item[1]}:{item[2]}' in checked:
                continue
            if nmap_exec is not None:
                command = ['nmap', '-Pn', '-p', item[2], item[1]]
                with sp.Popen(command, stdout=sp.PIPE) as process:
                    output = process.stdout.read()
                    if b' filtered ' in output:
                        logging.info(BFAIL_MSG, item[1], item[2], 'nmap:filtered')
                    elif b' closed ' in output:
                        logging.info(BFAIL_MSG, item[1], item[2], 'nmap:closed')
                    elif b' open ' in output:
                        logging.info(BSUCCESS_MSG, item[1], item[2])
                        fo.write(item[0])
                        fo.write('\n')
                        fo.flush()
                    else:
                        logging.error('Unrecognized output: %s', output.decode('ascii'))
            else:
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                    sock.settimeout(socket_timeout)
                    output = sock.connect_ex((item[1], int(item[2])))
                if output == 0:
                    logging.info(BSUCCESS_MSG, item[1], item[2])
                    fo.write(item[0])
                    fo.write('\n')
                    fo.flush()
                else:
                    logging.info(BFAIL_MSG, item[1], item[2],
                                 f'socket.connect_ex:{output}')
            checked.append(f'{item[1]}:{item[2]}')

## ------======| PARSER |======------

def create_parser():
    '''
    Create CLI arguments parser
    '''
    default_parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f'bricco {__version__}: Tor bridges testing tool',
        epilog=f'Bugtracker: {__bugtracker__}'
        )
    default_parser.add_argument('-v', '--version', action='version',
                                version=__version__)
    subparsers = default_parser.add_subparsers(title='Commands', dest='command')
    # test
    test_p = subparsers.add_parser('test', help=TEST_HELP)
    test_p.add_argument('-i', '--input', required=True, type=str,
                        dest='input_file', help='Input text file')
    test_p.add_argument('-o', '--output', required=True, type=str,
                        dest='output_file', help='Output text file')
    test_p.add_argument('-t', '--timeout', type=int, default=TIMEOUT_DEFAULT,
                        dest='socket_timeout', help=SOCKET_TIMEOUT_HELP)
    test_p.add_argument('-n', '--nmap', type=str, default=None,
                        dest='nmap_exec', help=NMAP_HELP)
    return default_parser

# -----=====| MAIN |=====-----

def main():
    '''
    Main function (entrypoint)
    '''
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    parser = create_parser()
    ns = parser.parse_args(sys.argv[1:])
    if ns.command == 'test':
        bricco_test(ns.input_file, ns.output_file, ns.socket_timeout,
                    ns.nmap_exec)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
