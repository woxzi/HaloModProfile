import sys
from zipfile import ZipFile
import configparser
from os.path import dirname, isfile
from os import altsep

project_root = dirname(__file__)

module_name = f'mod-profile'
module_version = 'v1.0'
config_path = f'{project_root}{altsep}profile.cfg'

print(config_path)

supported_commands = {
    'create': ('create', 2),
    'save': ('save <name>', 3),
    'load': ('load <name>', 3),
    'delete': ('delete <name>', 3),
    'status': ('status', 2),
    'help': ('help', 2),
    '?': ('?', 2)
}


def show_help():
    output = f"""
    === Halo Mod Profile Switcher {module_version} ===
    
    Available Commands:
    
    """
    for command, usage in supported_commands:
        output += f'\t{command}:\t{module_name} {usage}\n'

    print(output)


def invalid_command():
    output = 'Unrecognized command. Available commands:\n'
    for usage, expected_args in supported_commands.values():
        output += f'\t{module_name} {usage}\n'
    print(output)


def invalid_usage(command):
    output = f'Invalid usage of command \'{command}\'.\nUsage: {module_name} {supported_commands[command][0]}\n'
    print(output)


def create():
    pass


def save(profile):
    pass


def load(profile):
    pass


def delete(profile):
    pass


def status():
    pass


def init_app():
    welcome_message = f"=== Halo Mod Profile Switcher {module_version} ===\n\n" + \
                      "Welcome to the Halo Profile Switcher. To begin, please enter the path to your modding folder below:\n"
    working_directory = input(welcome_message)

    config = configparser.ConfigParser()
    config['Working Directories'] = {
        'default': working_directory
    }

    with open(config_path, 'w') as configfile:
        config.write(configfile)


if not isfile(config_path):
    init_app()
    exit()

num_commands = len(sys.argv)

command = None
command_args = None

if num_commands > 1:
    command = sys.argv[1]
if num_commands > 2:
    command_args = sys.argv[2:]

if len(sys.argv) < 2 or command not in supported_commands:
    invalid_command()
    exit()

elif command in supported_commands and len(sys.argv) != supported_commands[command][1]:
    invalid_usage(command)
    exit()

if command == 'create':
    pass
