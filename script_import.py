import os
import re
import sys
import logging
import sys
import inspect
import json

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
                imported_classes.add(clsmember)

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
class ScriptConfig(object):

    loaded_json = ""

    def __init__(self, filename):
        self.filename = filename

        try:
            data = open(self.filename).read()
            self.loaded_json = json.loads(data)
        except IOError:
            logging.critical("Error loading %s!", self.filename)
        else:
            logging.debug("Loaded %s" % (self.filename))

        self.check_valid_keys()
        self.create()

    def check_valid_keys(self):
        keys = self.loaded_json.keys()
        missing_keys = keys

        for classname, fullname in imported_classes:
            if classname in missing_keys:
                missing_keys.remove(classname)

        if len(missing_keys):
            missing_keys = ' '.join(missing_keys)
            logging.critical("Unknow scripts: %s in %s", missing_keys, self.filename)

    def create(self):
        keys = self.loaded_json.keys()
        for key in keys:
            for arr in self.loaded_json[key]:
                print arr
