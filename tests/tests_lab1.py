import unittest # unit testing framework
import subprocess # student code is run in a seperate process to isolate it from the test harness
from gradescope_utils.autograder_utils.decorators import weight, visibility # helper from gradescope to reformat the output from unittest to the JSON format gradescope wants

import shlex
import os

# Tests are put in a class. Each test starts test_ to allow them to be automatically discovered 
class TestStringOutput(unittest.TestCase):

    # setUp is run each time the testing framework is run so common actions put in here    
    def setUp(self):
        self.cpu_timeout = 100 # seconds
        self.username = os.environ['student_user']
        self.working_directory = '/autograder/student_code/'
        self.maxDiff = None
     
     
    # First test  
    @weight(1)
    @visibility('visible')
    def test_compile(self):
        command = 'make HelloWorld'
        proc = subprocess.Popen(shlex.split(command), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.working_directory, start_new_session=True, user=self.username)
        proc_stdout, proc_stderr = proc.communicate(timeout=self.cpu_timeout)        
        self.assertEqual(proc_stderr, '')
    test_compile.__doc__ = 'Test whether the file uploaded compiles'

    
    # Second test
    @weight(1)
    @visibility('visible')
    def test_hello_world(self):
        command = '/autograder/student_code/HelloWorld'
        proc = subprocess.Popen(shlex.split(command), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.working_directory, start_new_session=True, user=self.username)
        proc_stdout, proc_stderr = proc.communicate(timeout=self.cpu_timeout)        
        self.assertEqual(proc_stdout, 'Hello World')
    test_hello_world.__doc__ = 'Test whether the compiled program produces the correct text output'
    
    
    # System tests to check what works and what students can see
    @weight(1)
    @visibility('hidden')
    def test_cli(self):
        command = 'whoami > /autograder/results/results.test'
        #command = 'ping -c 2 bbc.co.uk'
        #command = 'ls /autograder/source/'
        proc = subprocess.Popen(shlex.split(command), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.working_directory, start_new_session=True, user=self.username)
        proc_stdout, proc_stderr = proc.communicate(timeout=self.cpu_timeout)
        self.assertEqual(proc_stdout, shlex.split(command))
    test_cli.__doc__ = 'Test what can be done in the test wrapper'
