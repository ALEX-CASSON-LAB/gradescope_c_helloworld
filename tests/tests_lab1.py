import unittest # unit testing framework
import subprocess32 as subprocess # student code is run in a seperate process to isolate it from the test harness
from gradescope_utils.autograder_utils.decorators import weight, visibility # helper from gradescope to reformat the output from unittest to the JSON format gradescope wants


# Tests are put in a class. Each test starts test_ to allow them to be automatically discovered 
class TestStringOutput(unittest.TestCase):

    # setUp is run each time the testing framework is run so common actions put in here    
    def setUp(self):
        self.cpu_timeout = 100 # seconds
     
     
    # First test  
    @weight(1)
    @visibility('visible')
    def test_compile(self):
        command = ['make', 'HelloWorld']
        result = subprocess.run(command, cwd='/autograder/source/student_code/', stdin=None, capture_output=True, text=True, timeout=self.cpu_timeout)
        self.assertEqual(result.stderr, '')
    test_compile.__doc__ = 'Test whether the file uploaded compiles'

    
    # Second test
    @weight(1)
    @visibility('visible')
    def test_hello_world(self):
        command = '/autograder/source/student_code/HelloWorld'
        result = subprocess.run(command, stdin=None, capture_output=True, text=True, timeout=self.cpu_timeout)
        self.assertEqual(result.stdout, 'Hello World')
    test_hello_world.__doc__ = 'Test whether the compiled program produces the correct text output'