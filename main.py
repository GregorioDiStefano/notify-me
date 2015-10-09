import script_importer
import time

script_importer.do_import("scripts", globals())

while True:
    for scripts in script_importer.imported_scripts:
        print eval(scripts).Test()
        time.sleep(60)
