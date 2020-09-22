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

def get_next_event(event_calendars):
    process = subprocess.run(add_calendar_parameter(
            ['gcalcli',  'agenda', '--military', 'now', 'next 3 months', '--tsv'], event_calendars),
            stdout=subprocess.PIPE,
            universal_newlines=True)
    agenda = process.stdout
    next_event = parse_event(agenda.splitlines()[0])
    dt = parse('{} {}'.format(next_event['date'], next_event['time']))
    return '{:%d.%m} {}'.format(dt, next_event['title'])

def show_month(month_calendars):
    subprocess.run(add_calendar_parameter([
        'xterm', '-bg', 'black', '-fg', 'white', '-title', 'i3blocks-gcalcli', '-hold', '-e',
        'gcalcli', 'calm', '--monday', '--military'],
        month_calendars))

def print_help():
    print('i3blocks_gcalcli.py -e <event_calendars> -m <month_calendars>')
    print('')
    print('Multiple calendars could be separated by comma.')
    print('Event calendars are considered when getting next upcoming event. Probably weather calendar should be skipped.')
    print('Month calendars are considered when showing full month after click.')

def main(argv):
    event_calendars = ''
    month_calendars = ''

    try:
        opts, args = getopt.getopt(argv, "he:m:",["eventCalendars=", "monthCalendars="])
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

    block_button = os.environ.get('BLOCK_BUTTON')
    if (block_button in ["1", "2", "3"]):
        show_month(month_calendars)

    print(get_next_event(event_calendars))


if __name__ == "__main__":
    main(sys.argv[1:])
