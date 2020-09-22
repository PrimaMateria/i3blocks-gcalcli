#!/usr/bin/python

import sys
import getopt
import os
import subprocess
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

def add_font_face_parameter(command, font_family):
    index = command.index('xterm') + 1
    command.insert(index, '-fa');
    index += 1
    command.insert(index, font_family)
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

def show_month(month_calendars, font_family):
    command = [ 'xterm', '-bg', 'black', '-fg', 'white', '-title', 'i3blocks-gcalcli', '-hold', '-e',
        'gcalcli', 'calm', '--monday', '--military']
    command = add_calendar_parameter(command, month_calendars)

    if font_family is not None:
        command = add_font_face_parameter(command, font_family)

    subprocess.run(command)

def print_help():
    print('Usage:')
    print('  i3blocks_gcalcli.py -e <event_calendars> -m <month_calendars> -f <font_family>')
    print('')
    print('Options:')
    print('  -e, --eventCalendars\t\t\tEvent calendars are considered when getting next upcoming event. Probably weather calendar should be skipped. Multiple values comma separated.')
    print('  -m, --montCalendars\t\t\tMonth calendars are considered when showing full month after click. Multiple values comma separated.')
    print('  -f, --fontFamily\t\t\tFont family/face used for xterm window showing month calendar.')

def main(argv):
    event_calendars = ''
    month_calendars = ''
    font_family = None

    try:
        opts, args = getopt.getopt(argv, "he:m:f:",["eventCalendars=", "monthCalendars=", "fontFamily="])
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

    block_button = os.environ.get('BLOCK_BUTTON')
    if (block_button in ["1", "2", "3"]):
        show_month(month_calendars, font_family)

    print(get_next_event(event_calendars))


if __name__ == "__main__":
    main(sys.argv[1:])
