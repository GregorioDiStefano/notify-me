import os
import re
import sys

import_blacklist = ["__init__", "Scripts"]
imported_scripts = set()

def do_import(path, env):
    sys.path.append(path)
    for module_name in sorted(__get_module_names_in_dir(path)):
        env[module_name] = __import__(module_name)

__module_file_regexp = "(.+)\.py$"

def __get_module_names_in_dir(path):
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            regexp_result = re.search(__module_file_regexp, entry)
            if regexp_result:
                module_name = regexp_result.groups()[0]
                if module_name in import_blacklist:
                    continue
                print "Loading: " , module_name
                imported_scripts.add(module_name)
    return imported_scripts
