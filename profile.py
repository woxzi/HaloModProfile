"""

Available commands:

new
save
load
delete
help

"""

import sys

module_name = 'mod-profile'

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
    output = """
    === Halo Mod Profile Switcher v1.0 ===
    
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


num_commands = len(sys.argv)

command = None
command_args = None

if num_commands > 1:
    command = sys.argv[1]
if num_commands > 2:
    command_args = sys.argv[2:]

if len(sys.argv) < 2 or command not in supported_commands:
    print(command)
    invalid_command()

elif command in supported_commands and len(sys.argv) != supported_commands[command][1]:
    invalid_usage(command)


