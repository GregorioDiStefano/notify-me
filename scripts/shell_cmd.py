from scripts import Scripts
import os
import subprocess
import shlex
import time
import logging

class ShellCmd(Scripts):
    cmd = ""
    filename = ""

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        self.filename = shlex.split(cmd)[0]

        if not self.test_script(self.filename):
            self.script_failed("File doesn't exist or is not executable")
            return None

        #pass remaining arguments to the parent class
        super(ShellCmd, self).__init__(**kwargs)

    def __str__(self):
        return "Shell Command: %s" % (self.cmd)

    #Simple, hacky (using type), check to see if cmd line is valid
    def test_script(self, filename):
        check_cmdline = "type %s 1>/dev/null" % (filename)
        if os.path.isfile(filename) and os.access(filename, os.X_OK):
            return True
        elif os.system(check_cmdline) == 0:
            return True
        return False

    def do_test(self):
        args = shlex.split(self.cmd)
        shell_script = subprocess.Popen(
            args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = shell_script.communicate()
        exit_code = shell_script.returncode

        if self.debug:
            logging.debug("Script out: " + out)

        if error or exit_code:
            self.failed(self.cmd)
        else:
            self.passed()
