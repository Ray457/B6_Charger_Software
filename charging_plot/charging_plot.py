"""
Parses the data from a B6 charger through a specified serial
port and save the voltage - time figure as a image file.
"""
import argparse
import os
import sys
import json
import serial
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    """
    Parses the command line arguments and extract the serial
    settings' file name.

    Args:
        None

    Returns:
        settings: dict, containing the args. Has:
            'config_file': string, file name of the config file
    """
    parser = argparse.ArgumentParser(
        description='Parses the data of a B6 charger and save the figure as a image file.')
    parser.add_argument('config_file', help='the file name for the serial settings')
    args = parser.parse_args()

    settings = {
        'config_file':args.config_file
        }
    return settings

def get_settings(filename):
    """
    may move into class Settings
    """
    settings = {}
    return settings

def save_settings(filename, settings):
    """
    may move into class Settings
    """
    pass

def open_serial():
    """
    to be done
    """
    ser = serial.Serial()
    return ser

def receive_data():
    """
    to be done
    """
    ser_data = np.array()
    return ser_data

def draw_plot():
    """
    to be done
    """
    pass

def save_plot():
    """
    to be done
    """
    pass

def cli_menus():
    """
    User interface in command line
    may get changed to handle UI only
    """
    settings = get_args()
    data = get_settings(settings['config_file'])
    if data == -1:
        if get_input(
                'Config file invalid. Create new settings?\nY/N ',
                ['', 'Y', 'y', 'N', 'n'],
                'Y').lower() == 'y':
            # save_settings(['config_file'], settings)
            pass

def get_input(prompt, expecting, default=None):
    """
    Reads user input from command line.

    Args:
        prompt: str, prompt showed to the user
        expecting: a sequence with all the expecting inputs
        default: default input value, defaults to None

    Returns:
        got: str, user input
    """
    got = ''
    while 1:
        if default is None:
            got = input(prompt)
        else:
            got = input("{}({})".format(prompt, default))
        if got in expecting:
            break
    if ('' in expecting) and (default is not None) and (got == ''):
        got = default
    return got

# main
def main():
    """
    Main function
    """
    cli_menus()

main()

# custom classes
class Settings:
    """
    to be done
    """
    __filename = ''
    __settings = {}
    __configfile_io = None

    def __init__(self, filename):
        self.__filename = filename
        self.__configfile_io = JsonIO(filename)

    def save_settings(self):
        """
        Saves the current settings into the config file,
        if it's not empty

        Returns:
            0: success
            -1: empty settings
            -2: file I/O error
        """
        if len(self.__settings) != 0:
            ret_code = JsonIO.write_file(self.__settings)
            return ret_code


class JsonIO:
    """
    Reads and writes json files
    """
    __filename = ''
    __fileObj = None
    def __init__(self, filename):
        self.__filename = filename

    def __validate_file(self):
        """
        Checks that the file actually exists and is not empty

        Args:
            None

        Returns:
            is_valid: boolean
        """
        if os.path.isfile(self.__filename):
            if not os.stat(self.__filename).st_size == 0: # check size
                return True

        return False

    def read_file(self):
        """
        Reads the <self.__filename> file as JSON.
        Invokes self.__validate_file()

        Args:
            None

        Returns:
            (ret_val, data)
            for ret_val:
                0: success
                -1: empty or non-existent file
                -2: incorrect format
                -3: other errors
            for data:
                None: error occurred
                otherwise result from json.loads()
        """
        if not self.__validate_file():
            return (-1, None)
        file = open(self.__filename, 'r')
        data = None

        try:
            data = json.loads(file.read())
        except ValueError:
            return (-2, None)
        except:
            return (-3, None)
        finally:
            file.close()
        return (0, data)

    def write_file(self, data):
        """
        Parses the data and write the content as JSON
        into the <self.__filename> file. Old contents
        will be ERASED.

        Args:
            data: can be int, str, dict, list etc, will
              be passed straight into json.dumps() so
              refer to the official docs for details

        Returns:
            0: success
            -1: error
        """
        file = open(self.__filename, 'w')

        try:
            file.write(json.dumps(data))
        except:
            return -1
        finally:
            file.close()
            return 0

class Queue:
    """
    A simple queue class implemented using linked list.
    Uses Node class.
    """
    __head_node = None
    __tail_node = None

    def __init__(self, init_item):
        self.__head_node = Node(init_item)

    def enqueue(self, item):
        """
        Enqueues an item into the end of queue

        Args:
            item: any object
        """
        if self.__tail_node is None:
            self.__tail_node = Node(item)
            self.__head_node.set_next(self.__tail_node)
        else:
            new_node = Node(item)
            self.__tail_node.set_next(new_node)
            self.__tail_node = new_node

    def dequeue(self):
        """
        Dequeues an item from the head of queue

        Returns:
            (ret_val, data)
            for ret_val:
                0: success
                -1: empty queue
            for data:
                None: error occurred
                otherwise item
        """
        if self.is_empty():
            return (-1, None)
        else:
            item = self.__head_node.get_data()
            self.__head_node = self.__head_node.get_next()
        return (0, item)

    def is_empty(self):
        """
        Returns True if the queue is empty
        """
        return self.__head_node is None

class Node:
    """
    Node class for linked lists
    """
    def __init__(self, init_data):
        self.data = init_data
        self.next = None

    def get_data(self):
        """
        Returns the data stored in the current node
        """
        return self.data

    def get_next(self):
        """
        Returns the next node
        """
        return self.next

    def set_data(self, new_data):
        """
        Sets the data stored in the current node
        """
        self.data = new_data

    def set_next(self, new_next):
        """
        Sets the next node
        """
        self.next = new_next
