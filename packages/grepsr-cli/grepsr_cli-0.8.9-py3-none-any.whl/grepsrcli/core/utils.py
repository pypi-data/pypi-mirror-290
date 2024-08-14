try:
    import readline # changes behavior of input()
except ImportError:
    pass # no pkg on windows.
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from os import listdir, path, mkdir
import re
from jinja2 import Template
import urllib.parse
from .config import load_config
from terminaltables import SingleTable
from .message_log import Log

PLATFORMS = ['php', 'php_next', 'node']
COMMENT_BLOCK_PATTERN = re.compile(r"(\/\*\*.?\n)(.*?)(\s*\*\/\s*\n)", re.DOTALL)
CLASS_DECLARATION_PATTERN = re.compile(r'class\s+\w+\s+extends\s(\w+)\b', re.DOTALL)

def get_plugin_path(plugin_name, type='php', all_types=False):
    """ returns the path of the plugin if plugin name exist

    Args:
        plugin_name (str): name of the service plugin .
        type (str, optional): php|py|node. Defaults to 'php'.
        all_types: retuns the path regardless the plugin types i.e php, py and node
    """
    config = load_config('config.yml')
    if all_types == False:
        if type == 'php':
            if _generate_plugin_path(plugin_name, config['php']['paths']):
                return _generate_plugin_path(plugin_name, config['php']['paths'])
            else:
                return False
        elif type == 'node':
            if _generate_plugin_path(plugin_name, config['node']['paths']):
                return _generate_plugin_path(plugin_name, config['node']['paths'])
            else:
                return False
        elif type == 'py':
            if _generate_plugin_path(plugin_name, config['python']['paths']):
                return _generate_plugin_path(plugin_name, config['python']['paths'])
            else:
                return False
        elif type == 'php_next':
            if _generate_plugin_path(plugin_name, config['php_next']['paths']):
                return _generate_plugin_path(plugin_name, config['php_next']['paths'])
            else:
                return False
        elif type == 'node_next':
            if _generate_plugin_path(plugin_name, config['node_next']['paths']):
                return _generate_plugin_path(plugin_name, config['node_next']['paths'])
            else:
                return False
        else:
            Log.error("Invalid params for type.")
            return False
    else:
        # todo: do not hardcode this
        base_paths_list = [
            config['php']['paths'] if 'php' in config else None,
            config['node']['paths'] if 'node' in config else None,
            config['python']['paths'] if 'python' in config else None,
            config['php_next']['paths'] if 'php_next' in config else None,
            config['node_next']['paths'] if 'node_next' in config else None
        ]

        for base_paths in base_paths_list:
            if base_paths is not None and _generate_plugin_path(plugin_name, base_paths):
                return _generate_plugin_path(plugin_name, base_paths)
        Log.error("Plugin name not found.")
        return False

def extract_plugin_properties(plugin_name):
    config = load_config('config.yml')
    plugin_properties = {
        'path': '',
        'type': '',
    }
    
    for platform in PLATFORMS:
        base_paths = config.get(platform, {}).get('paths', [])            
        abs_plugin_path = _generate_plugin_path(plugin_name, base_paths)
        if abs_plugin_path:
            plugin_properties['path'] = abs_plugin_path
            plugin_properties['type'] = platform
            break

    return plugin_properties

def get_extension(code_type='php'):
    if code_type == 'php':
        return 'php'
    elif code_type == 'node':
        return 'js'
    elif code_type == 'py':
        return 'py'
    elif code_type == 'php_next':
        return 'php'
    elif code_type == 'node_next':
        return 'js'
    else:
        Log.error("No extension for this type")
        return ''


def create_boilerplate(folder_path, boilerplate, data, extension, file_name = None):
    """ to create boilerplate for a given path

    Args:
        folder_path (str): the destination path
        boilerplate (str): the name of the boilerplate
        data (dict): the data to be rendered
    """
    if file_name is None:
        file_name = path.basename(folder_path)
    try:
        mkdir(folder_path)
    except OSError as err:
        Log.error(err)
        return

    dest_path = '{}/{}.{}'.format(folder_path, file_name, extension)

    render_boilerplate(boilerplate=boilerplate, data=data,
                       destination_path=dest_path)

    Log.info('Plugin created at {}'.format(dest_path))


def show_schema(base_path):
    """ this method will show the schema of a plugin if it has schema.json

    Args:
        base_path (str): the base path of the plugin  eg: /home/vtx-services/aaa_com/
    """

    schema_path = base_path + '/schema.json'
    if path.exists(schema_path):
        try:
            with open(schema_path, 'r') as f:
                schema = f.read()
                schema = json.loads(schema)
                for page in schema.keys():
                    Log.standout(f"Schema for Page: {page}")
                    schema_heading = ['field', 'type', 'pattern']
                    table_data = [
                        schema_heading
                    ]

                    for th, td in schema[page]['schema']['properties'].items():
                        if 'pattern' in td:
                            row = [th, td['type'], td['pattern']]
                        else:
                            row = [th, td['type'], '']

                        table_data.append(row)

                    print(SingleTable(table_data).table)
                return True
        except:
            Log.warn("Schema Structured Incorrectly")
    else:
        Log.warn("Schema Not Found")
        return False

def ask_user_input_YN(msg, default='Y'):
    while True:
        choice = input(msg + ' [Y/n]: ' if default == 'Y' else ' [y/N]: ').upper()
        if choice == 'N':
            return 'N'
        elif choice == 'Y':
            return 'Y'
        elif choice == '':
            return default

def ask_user_input(msg, allow_empty=False, raw_input=False):
    user_input = ''
    raw_inputs: List[str] = []
    while True:
        try:
            if raw_input:
                user_input = input(msg).strip()
                if not user_input and allow_empty:
                    break
                raw_inputs.append(user_input)
            else:
                user_input = input(msg).strip()
                if user_input or allow_empty:
                    break
        except EOFError:
            break
    if raw_input:
        user_input = '\n'.join(raw_inputs)
    return user_input

def generate_plugin_name(client_name, site_link, scrape_category = ''):
    plugin_standard_replacements = {
        r'\W+': '_',
    }
    
    client_name_standardized = re.sub(r'^[\s\.]*(.*)[\s\.]*$', '\\1', client_name)
    for pattern, repl in plugin_standard_replacements.items():
        client_name_standardized = re.sub(pattern, repl, client_name_standardized)

    only_host = extract_host_from_url(site_link) or ''
    for pattern, repl in plugin_standard_replacements.items():
        only_host = re.sub(pattern, repl, only_host)
    
    plugin_name_generated = [client_name_standardized, only_host, scrape_category]
    return '_'.join([e.lower() for e in plugin_name_generated if e])
    
def return_parsed_url(url) -> Optional[urllib.parse.ParseResult]:
    url = url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    try:
        return urllib.parse.urlparse(url)
    except ValueError:
        return None

def extract_host_from_url(url):
    parsed = return_parsed_url(url)
    if not parsed:
        return None
    hostname = parsed.netloc
    if hostname.startswith('www.'):
        hostname = hostname[4:]
    return hostname

def string_to_list(string) -> List[str]:
    parsed_list: List[str] = []
    if '\n' in string:
        parsed_list = string.split('\n')
    elif ',' in string:
        parsed_list = string.split(',')
    parsed_list = [e.strip() for e in parsed_list]
    return parsed_list

def list_dependencies(plugin_name):
    """list dependencies by listing all base_class"""

    dependencies = set()
    while True:
        plugin_dir_path = get_plugin_path(plugin_name)
        if not plugin_dir_path:
            break
        plugin_path = path.join(plugin_dir_path, plugin_name + '.php')
        contents = read_text(plugin_path)
        match = CLASS_DECLARATION_PATTERN.search(contents)
        if not match:
            break
        base_class = match.group(1)
        if base_class.startswith('Vtx_Service_Plugin'):
            break
        plugin_name = base_class
        dependencies.add(plugin_name)
    return list(dependencies)

def insert_all_chained_dependencies(plugin_name):
    """add dependencies if the dependencies follow service_code/service_code.php pattern, however deep"""

    dependencies = list_dependencies(plugin_name)
    plugin_dir_path = get_plugin_path(plugin_name)
    if not plugin_dir_path:
        return
    plugin_path = path.join(plugin_dir_path, plugin_name + '.php')
    contents = read_text(plugin_path)
    mappings = get_comment_block(contents)
    if 'Dependencies' not in mappings:
        mappings['Dependencies'] = ''
        original_deps = []
    else:
        original_deps = mappings['Dependencies'].split(',')
    
    mappings['Dependencies'] = ','.join(list(set(dependencies + original_deps)))
    contents = set_comment_block(contents, mappings)
    write_text(plugin_path, contents)
    return True

def set_comment_block(script, mappings):
    comment_block = ' * ' + '\n * '.join([f'{k}: {v}' for k, v in mappings.items()])
    subbed = COMMENT_BLOCK_PATTERN.sub('\\1' + comment_block + '\\3', script, 1)
    return subbed

def get_comment_block(script):
    match = COMMENT_BLOCK_PATTERN.search(script)
    if not match:
        return {}
    doc = match.group(2)
    lines = doc.splitlines()
    mappings = {}
    for line in lines:
        splitted = line.lstrip(' *').split(':', 1)
        if len(splitted) != 2:
            # TOOD: dont skip this,
            continue
        k, v = splitted
        mappings[k.strip()] = v.strip()
    return mappings

def first_found_numbers(text) -> str:
    match = re.search(r'(\d+)', text)
    if not match:
        return ''
    digit = match.group(1)
    return digit

def list_dependents(plugin_name):
    plugin_dir_path = get_plugin_path(plugin_name)
    repo_path = path.dirname(plugin_dir_path)
    dependents = []
    for directory in listdir(repo_path):
        plugin_path = path.join(repo_path, directory)
        if path.isfile(plugin_path):
            continue
        if get_plugin_info(plugin_path).get('base_class') == plugin_name:
            dependents.append(directory)
    return dependents

def get_plugin_info(plugin_path):
    """ get plugin's info like service_name,pid,description from the plugin's base folder.
    It does so by reading the file and looking at the info from plugin which is commented
    at the beginning.

    Args:
        plugin_path (str): the path of the directory where we find the plugin.
    """
    plugin_file_path = listdir(plugin_path)

    files = [f for f in plugin_file_path]
    plugin_file = ''
    for file in files:
        if path.basename(plugin_path) in file:
            plugin_file = file
            break

    if plugin_file:
        try:
            with open(path.join(plugin_path, plugin_file)) as f:
                script = f.read()
                match = CLASS_DECLARATION_PATTERN.search(script)
                base_class = None
                if match:
                    base_class = match[1]

                # TODO: use tree-sitter to parse php file.
                mappings = {k.upper(): v for k, v in get_comment_block(script).items()}
                if not mappings:
                    return {}
                dependencies_str = mappings.get('DEPENDENCIES', '')
                dependencies = [d.strip() for d in dependencies_str.split(',')]
                pid_line = mappings.get('PID', '')
                ssv = pid_line.split(' ')
                pid = ssv[0].strip()

                pid_forced = False
                if len(ssv) > 1:
                    pid_forced = ssv[1].strip() == 'force'
                
                # TODO: to parse php import mechanisms like require_once, include_once, etc. for dependencies 
                return {
                    'pid': pid,
                    'pid_forced': pid_forced,
                    'report_name': mappings.get('NAME'),
                    'description': mappings.get('DESCRIPTION'),
                    'dependencies': dependencies,
                    'base_class': base_class
                }
        except KeyError as e:
            pass
    return {}

def render_boilerplate(boilerplate, data, destination_path):
    """parse boilerplate from template directory to start a project

    Args:
        boilerplate (str): name of boilerplate template
        data (dict): input for the boilerplate
        destination_path: the final path where the final content needs to be saved
    """

    template_dir = Path(__file__).parent.parent.absolute()
    template_file = '{}/templates/{}'.format(template_dir, boilerplate)
    with open(template_file) as file:
        template = Template(file.read())
        with open(destination_path, 'w') as dest_file:
            dest_file.write(template.render(data))

def _generate_plugin_path(plugin_name, paths) -> Optional[str]:
    for service_path in paths:
        plugin_path = path.join(service_path, plugin_name)
        plugin_path = path.expanduser(plugin_path)
        if path.exists(plugin_path):
            return plugin_path

def get_docker_entrypoints(image_name):
    o = subprocess.run(f'docker inspect {image_name}', shell=True, capture_output=True, text=True)
    try:
        image_info = json.loads(o.stdout)
    except json.JSONDecodeError:
        raise Exception('Running docker inspect failed. Is SDK image correct?')
    try:
        return image_info[0]['Config']['Entrypoint']
    except IndexError:
        raise Exception('Docker inspect failed. Is Docker Running? Is SDK image available?')

def write_text(file_path, contents):
    "helper function to write text to file with compatible encoding and no newline magic"

    # turn off universal-newline mode for less surprises.
    with open(file_path, 'w', encoding='UTF-8', newline='') as fd:
        fd.write(contents)

def read_text(file_path):
    "helper function to read text from file with compatible encoding and no newline magic"

    # turn off universal-newline mode for less surprises.
    with open(file_path, 'r', encoding='UTF-8', newline='') as fd:
        contents = fd.read()

    return contents

def update_version_file(plugin_dir_path, major_flag, minor_flag):
    from semver import VersionInfo

    # create .version file or update .version file
    version_path = '{}/.version'.format(plugin_dir_path)
    if path.exists(version_path):
        version_info = VersionInfo.parse(read_text(version_path))
        if major_flag:
            version_info = version_info.next_version(
                part='major')
        elif minor_flag:
            version_info = version_info.next_version(
                part='minor')
        else:
            version_info = version_info.bump_patch()
        version_info = str(version_info)
    else:
        if major_flag:
            version_info = "1.0.0"
        elif minor_flag:
            version_info = "0.1.0"
        else:
            version_info = "0.0.1"

    write_text(version_path, version_info)

    return version_info

def return_cmd_with_progress(cmds, toolbar_width):
    try:
        multiplier = toolbar_width // len(cmds)
    except ZeroDivisionError:
        multiplier = 0
    # just echo some dashes after each command for progress. lol.
    echoer = 'echo -n ' + '-' * multiplier
    # .join() only does n-1 additions. Hence add a echoer at last. And then echo remaining to fill the bar (caused by floor division)
    cmd = f' && {echoer} &&'.join(cmds) + f' && {echoer}' + f' && echo -n {"-" * (toolbar_width - (len(cmds) * multiplier))}'
    return cmd

def is_path_tracked_by_git(relative_path, root_repo_dir):
    proc = cmd_shell_exec(f'git ls-files --error-unmatch {relative_path}', root_repo_dir)
    if proc.returncode == 0:
        return True
    return False

def does_plugin_have_modifications(plugin_name, root_repo_dir, crawler_type):
    """check if plugin has any modification in the code
    """
    if not is_path_tracked_by_git(f'{plugin_name}/', root_repo_dir):
        # is untracked file. meaning plugin was just created. it does have modifications.
        return True
    proc = cmd_shell_exec(f'git diff -s --exit-code {plugin_name}/{plugin_name}.{get_extension(crawler_type)}', root_repo_dir)
    if proc.returncode == 0:
        return False
    elif proc.returncode == 1:
        return True
    return None

def verbosify(cmds: List[str]) -> str:
    return ' && '.join([f'echo {cmd} && {cmd}' for cmd in cmds])

def cmd_shell_exec(cmd, working_dir, timeout=100):
    return subprocess.run(cmd, shell=True, timeout=timeout, cwd=working_dir, capture_output=True, text=True)

def get_current_branch_name(root_repo_dir: str) -> str:
    git_cmds = [
        'git branch --show-current',
        'git rev-parse --abbrev-ref HEAD',
        'git symbolic-ref --short HEAD',
    ]
    
    branch_name = ''
    for git_cmd in git_cmds:
        proc = cmd_shell_exec(git_cmd, root_repo_dir)
        if proc.returncode == 0:
            branch_name = proc.stdout.strip()
            break
    
    return branch_name

def load_json(json_str: str) -> Union[Dict[Any, Any], List[Any]]:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}