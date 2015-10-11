import os
import re
import sys
import logging
import sys
import inspect

#Forced to use this hack, since I cannot make scripts into a module
sys.path.append("scripts")
import scripts

import_blacklist = ["__init__"]
imported_scripts = set()
imported_classes = set()

def do_import(path, env):
    sys.path.append(path)
    for module_name in sorted(__get_module_names_in_dir(path)):
        env[module_name] = __import__(module_name)
        clsmembers = inspect.getmembers(sys.modules[str(module_name)], inspect.isclass)
        for clsmember in clsmembers:
            if issubclass(clsmember[1], scripts.Scripts):
                imported_classes.add(str(clsmember[1]))

__module_file_regexp = "(.+)\.py$"

def __get_module_names_in_dir(path):
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            regexp_result = re.search(__module_file_regexp, entry)
            if regexp_result:
                module_name = regexp_result.groups()[0]
                if module_name in import_blacklist:
                    continue
                logging.debug("Loading: " + module_name)
                imported_scripts.add(module_name)
    return imported_scripts

"""
    TODO:
    Read every section, and related key/value pairs, and create object from them
"""
class ScriptSettings(object):
    pass
