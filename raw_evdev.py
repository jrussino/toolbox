#!/usr/bin/env python
""" 
Linux utility for displaying raw input events (/dev/input/event*) 
"""
import argparse
import asyncio
import evdev
import sys


def get_device_info(device):
    """ Returns a string containing input device information.
        format: '<filename> "<name>" (<physical address>)' 
    """
    return '{} "{}" ({})'.format(device.fn, device.name, device.phys)


def select_device():
    """ Prompts user to select from a list of input devices.
        Returns an evdev InputDevice object corresponding to the selected device.
    """
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    print('### SELECT AN INPUT DEVICE ###')
    for i, device in enumerate(devices):
        print('[{}] {}'.format(i, get_device_info(device)))

    selected_device = None
    try:
        choice = int(input('>> '))
        if (choice in range(0, len(devices))):
            selected_device = devices[choice]
        else:
            print('ERROR - Invalid choice: {}'.format(choice))
    except Exception as e:
        print('Exception: {}'.format(e))

    return selected_device


async def print_events(device):
    """ Prints evdev input device events as they occur.
    """
    async for event in device.async_read_loop():
        if(event.code != 0):
            print('{}: {}'.format(evdev.categorize(event), event.value))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Displays raw events from HID-compatible input devices')
    parser.add_argument('-d', '--device', help='input device to open')
    args = parser.parse_args()

    if args.device is None:
        device = select_device()
        if device == None:
            sys.exit(-1)
    else:
        try:
            device = evdev.InputDevice(args.device)
        except Exception as e:
            print('Exception: {}'.format(e))
            sys.exit(-1)

    print('### DEVICE: {} ###'.format(get_device_info(device)))
    asyncio.ensure_future(print_events(device))
    loop = asyncio.get_event_loop()
    loop.run_forever()
