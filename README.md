# i3blocks gcalcli

Block for [i3blocks](https://github.com/vivien/i3blocks) which shows upcoming event in the status bar and full month when clicked on.

![screenshot](screenshot.png)

## Dependencies
- python
- [gcacli](https://github.com/insanum/gcalcli)
- [xterm](https://invisible-island.net/xterm/) - for showing calendar in popup window

## Installation
Install and setup gcalcli.

Setup popup window size and position in i3 config:
```
# i3blocks-gcalcli
for_window [class="XTerm" title="i3blocks-gcalcli"] floating enable
for_window [class="XTerm" title="i3blocks-gcalcli"] resize set 800 700 
for_window [class="XTerm" title="i3blocks-gcalcli"] move absolute position 1790 25
for_window [class="XTerm" title="i3blocks-gcalcli"] border none
```

## Usage

```
$ ./i3blocks_gcalcli.py -h
i3blocks_gcalcli.py -e <event_calendars> -m <month_calendars>

Multiple calendars could be separated by comma.
Event calendars are considered when getting next upcoming event. Probably weather calendar should be skipped.
Month calendars are considered when showing full month after click.
```

List blocklet configuration in i3blocks config:
```
[gcalcli]
command=i3blocks_gcalcli.py -e "Holidays in Germany" -m "weather,Holidays in Germany,Sviatky na Slovensku" 
interval=1800
```

