import sys
from zipfile import ZipFile
import configparser
from os.path import dirname, isfile, isdir, abspath
from os import altsep, getcwd, sep
import pathlib
import json
from shutil import rmtree

project_root = pathlib.Path(__file__).parent.resolve()

module_name = f'mod-profile'
status_file_name = f'.modprofiles'
module_version = 'v1.0'
config_path = f'{project_root}{sep}profile.cfg'

supported_commands = {
    'create': ('create', 2),
    'save': ('save <name>', 3),
    'load': ('load <name>', 3),
    'delete': ('delete <name>', 3),
    'status': ('status', 2),
    'help': ('help', 2),
    '?': ('?', 2)
}


def get_working_directory():
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['Working_Directories']['default']


def get_status_file_path():
    return get_working_directory() + sep + status_file_name


def save_status_file_config(config):
    with open(get_status_file_path(), 'w') as configfile:
        config.write(configfile)


def create_status_file():
    config = configparser.ConfigParser()
    config['Profiles'] = {
        'active': '*',
        'saved_profiles': '[]'
    }
    save_status_file_config(config)


def get_status_file():
    path = get_status_file_path()
    if not isfile(path):
        create_status_file()

    config = configparser.ConfigParser()
    config.read(path)
    return config


def show_help():
    output = f"""
    === Halo Mod Profile Switcher {module_version} ===
    
    Available Commands:
    
    """
    for command, (usage, expected_args) in supported_commands.items():
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
    base_path = get_working_directory()
    data_path = base_path + sep + 'data'
    data_archive_path = base_path + sep + 'data.zip'
    tags_path = base_path + sep + 'tags'
    tags_archive_path = base_path + sep + 'tags.zip'

    # process data folder
    if isdir(data_path):
        print(f'Deleting data folder: {data_path}')
        rmtree(data_path)

    print('Extracting data archive...')
    with ZipFile(data_archive_path, 'r') as zipObj:
        zipObj.extractall(base_path)
        print('Done.')

    # process tags folder
    if isdir(tags_path):
        print(f'Deleting tags folder: {tags_path}')
        rmtree(tags_path)

    print('Extracting tags archive...')
    with ZipFile(tags_archive_path, 'r') as zipObj:
        zipObj.extractall(base_path)
        print('Done.')

    config = get_status_file()
    config['Profiles']['active'] = '*'


def save(profile):
    if profile == '*':
        invalid_usage('save')
        print('Error: Cannot save to profile \'*\'')
        return

    config = get_status_file()

    # TODO save logic here

    profiles = json.loads(config['Profiles']['saved_profiles'])
    if not profile in profiles:
        profiles.append(profile)
        config['Profiles']['saved_profiles'] = json.dumps(profiles)
        save_status_file_config(config)


def load(profile):
    config = get_status_file()
    profiles = json.loads(config['Profiles']['saved_profiles'])

    if profile not in profiles:
        invalid_usage('load')
        print(f'Error: Cannot load from profile \'{profile}\'')
        return

    # TODO load logic here

    config = get_status_file()
    config['Profiles']['active'] = profile


def delete(profile):
    config = get_status_file()
    profiles = json.loads(config['Profiles']['saved_profiles'])

    if profile not in profiles:
        invalid_usage('delete')
        print(f'Error: Cannot delete profile \'{profile}\'')
        return

    # TODO delete logic here

    config = get_status_file()
    config['Profiles']['active'] = '*'


def status():
    config = get_status_file()
    profiles = json.loads(config['Profiles']['saved_profiles'])
    profile_list = ', '.join(profiles) if len(profiles) > 0 else 'None'
    active_profile = config['Profiles']['active'] if config['Profiles']['active'] != '*' else 'None'

    print(f"\tCurrent Profile: {active_profile}\n\tSaved Profiles: {profile_list}")


def init_app():
    welcome_message = f"=== Halo Mod Profile Switcher {module_version} ===\n\n" + \
                      "Welcome to the Halo Profile Switcher. To begin, please enter the path to your modding folder below:\n"
    working_directory = input(welcome_message)

    config = configparser.ConfigParser()
    config['Working_Directories'] = {
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
elif command in supported_commands and len(sys.argv) != supported_commands[command][1]:
    invalid_usage(command)
elif command.lower() == 'create':
    create()
elif command.lower() == 'load':
    load(command_args[0])
elif command.lower() == 'save':
    save(command_args[0])
elif command.lower() == 'delete':
    delete(command_args[0])
elif command.lower() == 'status':
    status()
elif command.lower() == '?' or command.lower() == 'help':
    show_help()
else:
    invalid_command()
