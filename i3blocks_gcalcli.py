#!/usr/bin/python

import sys
import getopt
import os
import subprocess
import math
from dateutil.parser import parse

def parse_event(line):
    tokens = line.split("\t")
    return {
        'date' : tokens[0],
        'time' : tokens[1],
        'title' : tokens[4]
        }

def add_calendar_parameter(command, calendars):
    index = command.index('gcalcli') + 1
    for calendar in calendars:
        command.insert(index, '--calendar')
        index += 1
        command.insert(index, calendar)
        index += 1
    return command

def add_xterm_parameter(command, param, value):
    index = command.index('xterm') + 1
    command.insert(index, param);
    index += 1
    command.insert(index, value)
    return command

def get_next_event(event_calendars):
    process = subprocess.run(add_calendar_parameter(
            ['gcalcli',  'agenda', '--military', 'now', 'next 3 months', '--tsv'], event_calendars),
            stdout=subprocess.PIPE,
            universal_newlines=True)
    agenda = process.stdout
    next_event = parse_event(agenda.splitlines()[0])
    dt = parse('{} {}'.format(next_event['date'], next_event['time']))
    return '{:%d.%m} {}'.format(dt, next_event['title'])

def show_month(month_calendars, font_family, width):
    right_border = 1
    left_border = 1
    days_on_row = 7 
    xterm_width = (width + left_border) * days_on_row + right_border

    calendar_command = ['gcalcli', 'calm', '--monday', '--military', '--width', str(width)]
    calendar_command = add_calendar_parameter(calendar_command, month_calendars)
    calendar_output = subprocess.check_output(calendar_command)

    height = len(calendar_output.splitlines())
    command = [ 'xterm', '-bg', 'black', '-fg', 'white', '-title', 'i3blocks-gcalcli', '-hold', '-e']
    command.extend(calendar_command)

    if font_family is not None:
        command = add_xterm_parameter(command, '-fa', font_family)

    if width is not None: 
        command = add_xterm_parameter(command, '-geometry', "{}x{}+0+0".format(xterm_width, height))

    subprocess.run(command)

def print_help():
    print('Usage:')
    print('  i3blocks_gcalcli.py -e <event_calendars> -m <month_calendars> -f <font_family>')
    print('')
    print('Options:')
    print('  -e, --eventCalendars\t\tEvent calendars are considered when getting next upcoming event. Probably weather calendar should be skipped. Multiple values comma separated.')
    print('  -m, --montCalendars\t\tMonth calendars are considered when showing full month after click. Multiple values comma separated.')
    print('  -f, --fontFamily\t\tFont family/face used for xterm window showing month calendar.')
    print('  -w, --width\t\t\tCell width of month calendar. Minimum 10. Default 20.')

def main(argv):
    event_calendars = ''
    month_calendars = ''
    font_family = None
    width = 20

    try:
        opts, args = getopt.getopt(argv, "he:m:f:w:",["eventCalendars=", "monthCalendars=", "fontFamily=", "width="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-e", "--eventCalendars"):
            event_calendars = arg.split(",")
        elif opt in ("-m", "--monthCalendars"):
            month_calendars = arg.split(",")
        elif opt in ("-f", "--fontFamily"):
            font_family = arg
        elif opt in ("-w", "--width"):
            width = int(arg)

    block_button = os.environ.get('BLOCK_BUTTON')
    if (block_button in ["1", "2", "3"]):
        show_month(month_calendars, font_family, width)

    print(get_next_event(event_calendars))


if __name__ == "__main__":
    main(sys.argv[1:])
