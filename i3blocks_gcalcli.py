#!/usr/bin/python

import sys
import getopt
import os
import subprocess
import math
from dateutil.parser import parse

statuses = ['datetimetitle', 'datetitle', 'title']

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

def get_next_event(event_calendars, status):
    process = subprocess.run(add_calendar_parameter(
            ['gcalcli',  'agenda', '--military', 'now', 'next 3 months', '--tsv'], event_calendars),
            stdout=subprocess.PIPE,
            universal_newlines=True)
    agenda = process.stdout
    next_event = parse_event(agenda.splitlines()[0])
    dt = parse('{} {}'.format(next_event['date'], next_event['time']))

    status_output = ''
    if (status == 'datetimetitle'):
        status_output = '{:%d.%m %H:%M} {}'.format(dt, next_event['title'])
    elif (status == 'datetitle'):
        status_output = '{:%d.%m} {}'.format(dt, next_event['title'])
    elif (status == 'title'):
        status_output = next_event['title']

    return status_output

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
    print('  i3blocks_gcalcli.py [options]')
    print('')
    print('Options:')
    print('  -e, --eventCalendars\t\tEvent calendars are considered when getting next upcoming event. Probably weather calendar should be skipped. Multiple values comma separated.')
    print('  -m, --monthCalendars\t\tMonth calendars are considered when showing full month after click. Multiple values comma separated.')
    print('  -f, --fontFamily\t\tFont family/face used for xterm window showing month calendar.')
    print('  -w, --width\t\t\tCell width of month calendar. Minimum 10. Default 20.')
    print('  -s, --status\t\t\tStatus format. Possible values: datetimetitle, datetitle, title. Default datetimetitle.')

def main(argv):
    event_calendars = ''
    month_calendars = ''
    font_family = None
    width = 20
    status = 'datetimetitle'

    try:
        opts, args = getopt.getopt(argv, "he:m:f:w:s:",["eventCalendars=", "monthCalendars=", "fontFamily=", "width=", "status="])
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
        elif opt in ("-s", "--status"):
            if (arg not in statuses):
                print_help();
                sys.exit(2)
            status = arg

    block_button = os.environ.get('BLOCK_BUTTON')
    if (block_button in ["1", "2", "3"]):
        show_month(month_calendars, font_family, width)

    print(get_next_event(event_calendars, status))


if __name__ == "__main__":
    main(sys.argv[1:])
