# Import needed modules
import unittest # unit testing framework
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner # helper from gradescope to reformat the output from unittest to the JSON format gradescope wants
from tests.tests_lab1 import TestStringOutput # import my tests
try: # used to secure the computer, e.g. remove network access
    import seccomp
except ImportError:
    import pyseccomp as seccomp
import socket # needed to remove network access for security
import errno # make standard error systems avaialable to improve reporting
import resource # used to restrict access to system resources, over and above the gradescope container constraints
from io import StringIO # used to redirect the standard error so not displayed by default
import sys # used to give access to system parts (mainly stdin, etc.)



# Function to limit access to system resources
def set_limits():
    # There are a number of other things that can be restricted with resource, see https://docs.python.org/3/library/resource.html, and with seccomp see https://healeycodes.com/running-untrusted-python-code. Here we only do the main ones and rely on the container to restrict anything else. Note that CPU timeouts are implemented in the tests using the subprocess module rather than done at a high level here

    # virtual memory
    memory_limit = 524288000 # bytes (so 500 MB)
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    
    # write limit i.e. don't allow an infinite stream to stdout/stderr
    write_limit = 10485760 # bytes (so 10 MB)
    resource.setrlimit(resource.RLIMIT_FSIZE, (write_limit, write_limit))
    
    # System calls are allowed, would be more secure with an allow list of calls, but the calls used might vary with the code that people submit and do defining the allow list needs care. Can turn all off with: filter = seccomp.SyscallFilter(seccomp.ERRNO(seccomp.errno.EPERM))
    filter = seccomp.SyscallFilter(seccomp.ALLOW) 
    
    # Turn off network access
    for network in [socket.AF_INET, socket.AF_INET6]:
        filter.add_rule(
            seccomp.ERRNO(errno.EACCES),
            "socket",
            seccomp.Arg(0, seccomp.EQ, network),
        )
        
    # Apply seccomp filters
    filter.load()
  
  

# Run the tests
if __name__ == '__main__':

    # Apply security settings
    set_limits()

    # Run tests
    temp_stderr = StringIO() # test runner displays results on stderr. We log this to a variable to reduce the chance aof nything appearing on stdout gets logged by mistake
    sys.stderr = temp_stderr
    suite = unittest.defaultTestLoader.discover('tests')
    JSONTestRunner(stream=sys.stderr).run(suite)
    print(temp_stderr.getvalue())
    sys.stderr = sys.__stderr__ # reset stderr