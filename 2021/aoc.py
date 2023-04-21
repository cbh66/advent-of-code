#!/usr/bin/python3

import sys
import os
import subprocess
import json
import getopt
import requests
from shutil import copyfile
from datetime import date

YEAR = 2021
EXTENSION = '.py'
INPUT_DIR = 'inputs'
PROGRAM_DIR = 'programs'
CONFIG_FILE = '.aocconfig'

def option_value(options, keys):
    for key, val in options:
        if key in keys:
            return val
    return None

def write_cookie(cookie):
    with open(CONFIG_FILE, 'w+') as f:
        json.dump({ 'cookie': cookie }, f)

def read_cookie():
    with open(CONFIG_FILE, 'r') as f:
        contents = json.load(f)
        return contents['cookie']

def day_of_december():
    today = date.today()
    if today.month != 12:
        raise Exception('It is not December, so cannot infer which puzzle to run. Supply an argument with --day')
    if not 1 <= today.day <= 25:
        raise Exception('It is not between December 1 and 25, so cannot infer which puzzle to run. Supply and argument with --day')
    return today.day

def input_file_name(day):
    return f'{INPUT_DIR}/{day}.txt'

def program_file_name(day, part):
    return f'{PROGRAM_DIR}/{day}-{part}{EXTENSION}'

def setup_program_for_day(day, part):
    if part == 'b':
        copyfile(program_file_name(day, 'a'), program_file_name(day, 'b'))
        
    elif part == 'a':
        with open(program_file_name(day, 'a'), 'w+') as f:
            f.write("""#!/usr/bin/python3

import sys

def main(inputs):
    pass

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
""")
    os.chmod(program_file_name(day, part), 0o777)

def get_inputs_for_day(day, cookie):
    url = f"https://adventofcode.com/{YEAR}/day/{day}/input"
    r = requests.get(url, cookies={ 'session': cookie })
    with open(input_file_name(day), 'wb+') as f:
        f.write(r.content)

def run_puzzle(program_file, input=None):
    subprocess.run([program_file], stdin=input)

# options
# {num} or --day {num} (if omitted, uses today if between dec 1-25).
# -p {a|b} or --part {a|b} (if omitted, uses a).
# -i or --interactive allows you to supply stdin to the program instead of using the input file.
# --init creates a new program file instead of running the program. For part b, it copies part a into a new file.
# --cookie {cookie} uses and saves the cookie to use for downloading input files. This only needs to be done once, or if the cookie changes.
def main(args, options):
    # parse args, figure out day
    day = option_value(options, ['--day'])
    if day is not None:
        day = int(day)
    else:
        day = int(args[0]) if len(args) > 0 else day_of_december()
    if not 1 <= day <= 25:
        raise ValueError(f"'day' must be between 1 and 25, received {day}")

    part = option_value(options, ['-p', '--part'])
    if part is None:
        part = 'a'
    if part not in ['a', 'b']:
        raise ValueError(f"'part' must be 'a' or 'b', received '{part}'")

    cookie = option_value(options, ['--cookie'])
    if cookie is not None:
        write_cookie(cookie)
    else :
        try:
            cookie = read_cookie()
        except Exception:
            print('No cookie found. Get your session cookie from dev tools on the advent of code site, then run this script again with the --cookie option (you only need to do this once, or when your cookie changes)')
            raise

    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(PROGRAM_DIR, exist_ok=True)

    if not os.path.isfile(input_file_name(day)):
        get_inputs_for_day(day, cookie)

    if option_value(options, ['--init']) is not None:
        setup_program_for_day(day, part)
        return

    is_interactive = option_value(options, ['-i', '--interactive'])
    is_interactive = False if is_interactive is None else True
    print(f"Running puzzle for day {day}, part {part}\n\n")
    if is_interactive:
        print('in interactive mode')
        run_puzzle(program_file_name(day, part))
    else:
        with open(input_file_name(day), 'r') as f:
            run_puzzle(program_file_name(day, part), f)
    
if __name__ == "__main__":
    options, args = getopt.getopt(sys.argv[1:], 'ip:', ['day=', 'part=', 'cookie=', 'init', 'interactive'])
    main(args, options)
