import sys
import getopt
import os
import subprocess
import math
import click
from dateutil.parser import parse

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
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

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="1.0.0")
def main():
    pass

@cli.command()
@click.option("-e", "--eventCalendars", default="", help="Event calendars are considered when getting next upcoming event. Probably weather calendar should be skipped. Multiple values comma separated.")
@click.option("-m", "--monthCalendars", default="", help="Month calendars are considered when showing full month after click. Multiple values comma separated.")
@click.option("-f", "--fontFamily", default=None, help="Font family/face used for xterm window showing month calendar.")
@click.option("-w", "--width", default=20, type=int, help="Cell width of month calendar. Minimum 10.")
@click.option("-s", "--status", default="datetimetitle",  type=click.Choice(['datetimetitle', 'datetitle', 'titlte'], help="Status format.")
def print(**kwargs):
    event_calendars = kwargs["eventCalendars"].split(",")
    month_calendars = kwargs["monthCalendars"].split(",")
    font_family = kwargs["fontFamily"]
    width = kwargs["width"]
    status = kwargs["status"]

    print(event_calendars)
    print(month_calendars)
    print(font_family)
    print(width)
    print(status)

    # block_button = os.environ.get('BLOCK_BUTTON')
    # if (block_button in ["1", "2", "3"]):
        # show_month(month_calendars, font_family, width)

    # print(get_next_event(event_calendars, status))


if __name__ == "__main__":
    main()
