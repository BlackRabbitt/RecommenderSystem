﻿#! /usr/bin/env python
#coding: utf-8

'''
COPYRIGHT (c) 2009, 2010, 2011, 2012
.. in order of first contribution
Olof Bjarnason
    Initial proof-of-concept pygame implementation.
Fredrik Wendt
    Help with Tkinter implementation (replacing the pygame dependency)
Krunoslav Saho
    Added always-on-top to the pytddmon window
Samuel Ytterbrink
    Print(".") will not screw up test-counting (it did before)
    Docstring support
    Recursive discovery of tests
    Refactoring to increase Pylint score from 6 to 9.5 out of 10 (!)
    Numerous refactorings & other improvements
Rafael Capucho
    Python shebang at start of script, enabling "./pytddmon.py" on unix systems
Ilian Iliev
    Use integers instead of floats in file modified time (checksum calc)
    Auto-update of text in Details window when the log changes

LICENSE
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import os
import sys
import platform
import optparse
import re
import unittest
import doctest
import time
import multiprocessing
import fnmatch
import functools

ON_PYTHON3 = sys.version_info[0] == 3
ON_WINDOWS = platform.system() == "Windows"

####
## Core
####

class Pytddmon:
    "The core class, all functionality is combined into this class"
    def __init__(
        self,
        file_finder,
        monitor,
        project_name = "<pytddmon>"
    ):
        self.file_finder = file_finder
        self.project_name = project_name
        self.monitor = monitor
        self.change_detected = False

        self.total_tests_run = 0
        self.total_tests_passed = 0
        self.last_testrun_time = -1
        self.log = ""

        self.run_tests()

    def run_tests(self):
        """Runs all tests and updates state variables with results."""
        
        file_paths = self.file_finder()
        
        # We need to run the tests in a separate process, since
        # Python caches loaded modules, and unittest/doctest
        # imports modules to run them.
        # However, we do not want to assume users' unit tests
        # are thread-safe, so we only run one test module at a
        # time, using processes = 1.
        start = time.time()
        if file_paths:
            pool = multiprocessing.Pool(processes = 1)
            results = pool.map(run_tests_in_file, file_paths)
            pool.close()
            pool.join()
        else:
            results = []
        self.last_testrun_time = time.time() - start
        
        now = time.strftime("%H:%M:%S", time.localtime())
        self.log = ""
        self.log += "Monitoring folder %s.\n" % self.project_name
        self.log += "Found <TOTALTESTS> tests in %i files.\n" % len(results)
        self.log += "Last change detected at %s.\n" % now
        self.log += "Test run took %.2f seconds.\n" % self.last_testrun_time
        self.log += "\n"
        self.total_tests_passed = 0
        self.total_tests_run = 0
        for packed in results:
            (module, green, total, logtext) = packed
            self.total_tests_passed += green
            self.total_tests_run += total
            self.log += "\nLog from " + module + ":\n" + logtext
        self.log = self.log.replace('<TOTALTESTS>', str(int(self.total_tests_run.real)))

    def main(self):
        """This is the main loop body"""
        self.change_detected = self.monitor.look_for_changes()
        if self.change_detected:
            self.run_tests()

    def get_log(self):
        """Access the log string created during test run"""
        return self.log

class Monitor:
    'Looks for file changes when prompted to'
    
    def __init__(self, file_finder, get_file_size, get_file_modtime):
        self.file_finder = file_finder
        self.get_file_size = get_file_size
        self.get_file_modtime = get_file_modtime
        self.snapshot = self.get_snapshot()

    def get_snapshot(self):
        snapshot = {}
        for file in self.file_finder():
            file_size = self.get_file_size(file)
            file_modtime = self.get_file_modtime(file)
            snapshot[file] = (file_size, file_modtime)
        return snapshot

    def look_for_changes(self):
        new_snapshot = self.get_snapshot()
        change_detected = new_snapshot != self.snapshot
        self.snapshot = new_snapshot
        return change_detected


####
## Finding files
####

class FileFinder:
    "Returns all files matching given regular expression from root downwards"
    
    def __init__(self, root, regexp):
        self.root = os.path.abspath(root)
        self.regexp = regexp
        
    def __call__(self):
        return self.find_files()

    def find_files(self):
        "recursively finds files matching regexp"
        file_paths = set()
        for path, _folder, filenames in os.walk(self.root):
            for filename in filenames:
                if self.re_complete_match(filename):
                    file_paths.add(
                        os.path.abspath(os.path.join(path, filename))
                    )
        return file_paths
        
    def re_complete_match(self, string_to_match):
        "full string regexp check"
        return bool(re.match(self.regexp + "$", string_to_match))

wildcard_to_regex = fnmatch.translate

####
## Finding & running tests
####

def log_exceptions(func):
    """Decorator that forwards the error message from an exception to the log
    slot of the return value, and also returns a complexnumber to signal that
    the result is an error."""
    wraps = functools.wraps

    @wraps(func)
    def wrapper(*a, **k):
        "Docstring"
        try:
            return func(*a, **k)
        except:
            import traceback
            return ('', 0, 1j, traceback.format_exc())
    return wrapper

@log_exceptions
def run_tests_in_file(file_path):
    module = file_name_to_module("", file_path)
    return run_module(module)

def run_module(module):
    suite = find_tests_in_module(module)
    (green, total, log) = run_suite(suite)
    return (module, green, total, log)

def file_name_to_module(base_path, file_name):
    r"""Converts filenames of files in packages to import friendly dot
    separated paths.

    Examples:
    >>> print(file_name_to_module("","pytddmon.pyw"))
    pytddmon
    >>> print(file_name_to_module("","pytddmon.py"))
    pytddmon
    >>> print(file_name_to_module("","tests/pytddmon.py"))
    tests.pytddmon
    >>> print(file_name_to_module("","./tests/pytddmon.py"))
    tests.pytddmon
    >>> print(file_name_to_module("",".\\tests\\pytddmon.py"))
    tests.pytddmon
    >>> print(
    ...     file_name_to_module(
    ...         "/User/pytddmon\\ geek/pytddmon/",
    ...         "/User/pytddmon\\ geek/pytddmon/tests/pytddmon.py"
    ...     )
    ... )
    tests.pytddmon
    """
    symbol_stripped = os.path.relpath(file_name, base_path)
    for symbol in r"/\.":
        symbol_stripped = symbol_stripped.replace(symbol, " ")
    words = symbol_stripped.split()
    # remove .py/.pyw
    module_words = words[:-1]
    module_name = '.'.join(module_words)
    return module_name

def find_tests_in_module(module):
    suite = unittest.TestSuite()
    suite.addTests(find_unittests_in_module(module))
    suite.addTests(find_doctests_in_module(module))
    return suite

def find_unittests_in_module(module):
    test_loader = unittest.TestLoader()
    return test_loader.loadTestsFromName(module)

def find_doctests_in_module(module):
    try:
        return doctest.DocTestSuite(module, optionflags = doctest.ELLIPSIS)
    except ValueError:
        return unittest.TestSuite()

def run_suite(suite):
    def StringIO():
        if ON_PYTHON3:
            import io as StringIO
        else:
            import StringIO 
        return StringIO.StringIO()
    err_log = StringIO()
    text_test_runner = unittest.TextTestRunner(stream = err_log, verbosity = 1)
    result = text_test_runner.run(suite)
    green = result.testsRun - len(result.failures) - len(result.errors)
    total = result.testsRun
    log = err_log.getvalue() if green<total else "All %i tests passed\n" % green
    return (green, total, log)


####
## GUI
####


class TkGUI(object):
    """Connect pytddmon engine to Tkinter GUI toolkit"""
    def __init__(self, pytddmon):
        self.pytddmon = pytddmon
        self.color_picker = ColorPicker()
        self.tkinter = None
        self.building_tkinter()
        self.root = None
        self.building_root()
        self.title_font = None
        self.button_font = None
        self.building_fonts()
        self.frame = None
        self.building_frame()
        self.button = None
        self.building_button()
        self.frame.grid()
        self.message_window = None
        self.text = None

        if ON_WINDOWS:
            buttons_width = 25
        else:
            buttons_width = 75
        self.root.minsize(
            width=self.title_font.measure(
                self.pytddmon.project_name
            ) + buttons_width, 
            height=0
        )
        self.frame.pack(expand=1, fill="both")

    def building_tkinter(self):
        """imports the tkinter module as self.tkinter"""
        if not ON_PYTHON3:
            import Tkinter as tkinter
        else:
            import tkinter
        self.tkinter = tkinter

    def building_root(self):
        """take hold of the tk root object as self.root"""
        self.root = self.tkinter.Tk()
        self.root.wm_attributes("-topmost", 1)
        if ON_WINDOWS:
            self.root.attributes("-toolwindow", 1)
            print("Minimize me!")

    def building_fonts(self):
        "building fonts"
        if not ON_PYTHON3:
            import tkFont
        else:
            from tkinter import font as tkFont 
        self.title_font = tkFont.nametofont("TkCaptionFont")
        self.button_font = tkFont.Font(name="Helvetica", size=28)

    def building_frame(self):
        """Creates a frame and assigns it to self.frame"""
        # Calculate the width of the tilte + buttons
        self.frame = self.tkinter.Frame(
            self.root
        )
        # Sets the title of the gui
        self.frame.master.title(self.pytddmon.project_name)
        # Forces the window to not be resizeable
        self.frame.master.resizable(False, False)
        self.frame.pack(expand=1, fill="both")

    def building_button(self):
        """Builds  abutton and assign it to self.button"""
        self.button = self.tkinter.Label(
            self.frame,
            text="loading...",
            relief='raised',
            font=self.button_font,
            justify=self.tkinter.CENTER,
            anchor=self.tkinter.CENTER
        )
        self.button.bind(
            "<Button-1>",
            self.display_log_message
        )
        self.button.pack(expand=1, fill="both")

    def window_is_open(self):
        """checks whether the textwdiget windows is open"""
        if not self.message_window or not self.message_window.winfo_exists():
            return False
        return True

    def update(self):
        """updates the tk gui"""
        self.color_picker.set_result(
            self.pytddmon.total_tests_passed,
            self.pytddmon.total_tests_run,
        )
        light, color = self.color_picker.pick()
        rgb = self.color_picker.translate_color(light, color)
        self.color_picker.pulse()
        if self.pytddmon.total_tests_run.imag!=0:
            text = "?ERROR"
        else:
            text = "%r/%r" % (
                self.pytddmon.total_tests_passed,
                self.pytddmon.total_tests_run
            )

        self.button.configure(
            bg=rgb,
            activebackground=rgb,
            text=text
        )
        self.root.configure(
            bg=rgb,
        )
        
        if self.pytddmon.change_detected and self.window_is_open():
            self.update_text_window()

    def get_text_message(self):
        """returns the logmessage from pytddmon"""
        message = self.pytddmon.get_log()
        return message

    def open_text_window(self):
        """creates new window and text widget""" 
        win = self.tkinter.Toplevel()
        win.wm_attributes("-topmost", 1)
        if ON_WINDOWS:
            win.attributes("-toolwindow", 1)
        win.title('Details')
        self.message_window = win
        self.text = self.tkinter.Text(win)

    def update_text_window(self):
        """inserts/replaces the log message in the text widget"""
        text = self.text
        text['state'] = self.tkinter.NORMAL
        text.delete(1.0, self.tkinter.END)
        text.insert(self.tkinter.INSERT, self.get_text_message())
        text['state'] = self.tkinter.DISABLED
        text.pack(expand=1, fill='both')
        text.focus_set()

    def display_log_message(self, _arg):
        """displays the logmessage from pytddmon in a window"""
        if not self.window_is_open():
            self.open_text_window()
            self.update_text_window()

    def loop(self):
        """the main loop"""
        self.pytddmon.main()
        self.update()
        self.frame.after(750, self.loop)

    def run(self):
        """starts the main loop and goes into sleep"""
        self.loop()
        self.root.mainloop()

class ColorPicker:
    """
    ColorPicker decides the background color the pytddmon window,
    based on the number of green tests, and the total number of
    tests. Also, there is a "pulse" (light color, dark color),
    to increase the feeling of continous testing.
    """
    color_table = {
        (True, 'green'): '0f0',
        (False, 'green'): '0c0',
        (True, 'red'): 'f00',
        (False, 'red'): 'c00',
        (True, 'orange'): 'fc0',
        (False, 'orange'): 'ca0',
        (True, 'gray'): '999',
        (False, 'gray'): '555'
    }

    def __init__(self):
        self.color = 'green'
        self.light = True

    def pick(self):
        "returns the tuple (light, color) with the types(bool ,str)"
        return (self.light, self.color)

    def pulse(self):
        "updates the light state"
        self.light = not self.light

    def reset_pulse(self):
        "resets the light state"
        self.light = True

    def set_result(self, green, total):
        "calculates what color should be used and may reset the lightness"
        old_color = self.color
        self.color = 'green'
        if green.imag or total.imag:
            self.color = "orange"
        elif green == total - 1:
            self.color = 'red'
        elif green < total - 1:
            self.color = 'gray'
        if self.color != old_color:
            self.reset_pulse()

    @classmethod
    def translate_color(cls, light, color):
        """helper method to create a rgb string"""
        return "#" + cls.color_table[(light, color)]


def parse_commandline():
    """
    returns (files, test_mode) created from the command line arguments
    passed to pytddmon.
    """
    parser = optparse.OptionParser()
    parser.add_option(
        "--log-and-exit",
        action="store_true",
        default=False,
        help='Run all tests, write the results to "pytddmon.log" and exit.')
    (options, args) = parser.parse_args()
    return (args, options.log_and_exit)

def build_monitor(file_finder):
    os.stat_float_times(False)
    def get_file_size(file_path):
        stat = os.stat(file_path)
        return stat.st_size
    def get_file_modtime(file_path):
        stat = os.stat(file_path)
        return stat.st_mtime
    return Monitor(file_finder, get_file_size, get_file_modtime)

def run():
    """
    The main function: basic initialization and program start
    """
    cwd = os.getcwd()
    
    # Include current work directory in Python path
    sys.path[:0] = [cwd]
    
    # Command line argument handling
    (static_file_set, test_mode) = parse_commandline()
    
    # What files to monitor?
    if not static_file_set:
        regex = wildcard_to_regex("*.py")
    else:
        regex = '|'.join(static_file_set)
    file_finder = FileFinder(cwd, regex)
    
    # The change detector: Monitor
    monitor = build_monitor(file_finder)
    
    # Python engine ready to be setup
    pytddmon = Pytddmon(
        file_finder,
        monitor,
        project_name = os.path.basename(cwd)
    )
    
    # Start the engine!
    if not test_mode:
        TkGUI(pytddmon).run()
    else:
        pytddmon.main()
        with open("pytddmon.log", "w") as log_file:
            log_file.write(
                "green=%r\ntotal=%r\n" % (
                    pytddmon.total_tests_passed,
                    pytddmon.total_tests_run
                )
            )

if __name__ == '__main__':
    run()
