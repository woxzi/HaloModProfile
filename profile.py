import sys
from zipfile import ZipFile
import configparser
from os.path import dirname, isfile, isdir, abspath
from os import altsep, getcwd, sep, makedirs
import pathlib
import json
from shutil import rmtree, copytree

project_root = pathlib.Path(__file__).parent.resolve()

module_name = 'mod-profile'
status_file_name = '.modprofiles'
profile_folder_name = 'modprofiles'
module_version = 'v1.0'
config_path = f'{project_root}{sep}profile.cfg'
empty_profile = '*'

supported_commands = {
    'create': ('create', 2, 2),
    'reset': ('reset', 2, 2),
    'save': ('save <name>', 2, 3),
    'load': ('load <name>', 3, 3),
    'delete': ('delete <name>', 3, 3),
    'status': ('status', 2, 2),
    'help': ('help', 2, 2),
    '?': ('?', 2, 2)
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
        'active': empty_profile,
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
    for command, (usage, min_expected_args, max_expected_args) in supported_commands.items():
        output += f'\t{command}:\t{module_name} {usage}\n'

    print(output)


def invalid_command():
    output = 'Unrecognized command. Available commands:\n'
    for usage, min_expected_args, max_expected_args in supported_commands.values():
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

    # set current profile to none
    config = get_status_file()
    config['Profiles']['active'] = empty_profile


def save(profile=None):
    config = get_status_file()
    if profile == empty_profile:
        invalid_usage('save')
        print(f'Error: Cannot save to profile \'{empty_profile}\'')
        return
    elif profile is None and config['Profiles']['active'] == empty_profile:
        invalid_usage('save')
        print('Error: Cannot save to empty profile')
        return

    active_profile = profile if profile is not None else config['Profiles']['active']

    base_path = get_working_directory()
    profile_path = base_path + sep + profile_folder_name + sep + active_profile
    data_path = sep + 'data'
    tags_path = sep + 'tags'

    if isdir(profile_path):
        rmtree(profile_path)
    makedirs(profile_path)

    def save_folder(extension):
        copytree(base_path + extension, profile_path + extension)

    save_folder(data_path)
    save_folder(tags_path)

    # add profile to saved profile list and switch to it
    profiles = json.loads(config['Profiles']['saved_profiles'])
    if not active_profile in profiles:
        profiles.append(active_profile)
        config['Profiles']['saved_profiles'] = json.dumps(profiles)
    config['Profiles']['active'] = active_profile
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
    config['Profiles']['active'] = empty_profile


def status():
    config = get_status_file()
    profiles = json.loads(config['Profiles']['saved_profiles'])
    profile_list = ', '.join(profiles) if len(profiles) > 0 else 'None'
    active_profile = config['Profiles']['active'] if config['Profiles']['active'] != empty_profile else 'None'

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
    command_args = sys.argv[2:]

if num_commands == 1:
    show_help()
elif len(sys.argv) < 2 or command not in supported_commands:
    invalid_command()
elif command in supported_commands and not (supported_commands[command][1] <= len(sys.argv) <= supported_commands[command][2]):
    invalid_usage(command)
elif command.lower() == 'create' or command.lower() == 'reset':
    create()
elif command.lower() == 'load':
    load(command_args[0])
elif command.lower() == 'save':
    if len(command_args) > 0:
        save(command_args[0])
    else:
        save()
elif command.lower() == 'delete':
    delete(command_args[0])
elif command.lower() == 'status':
    status()
elif command.lower() == '?' or command.lower() == 'help':
    show_help()
else:
    invalid_command()
