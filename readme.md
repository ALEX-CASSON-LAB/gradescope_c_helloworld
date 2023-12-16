Overview
--------
A "Hello World" example for Gradescope (https://gradescope-autograders.readthedocs.io/en/latest/). There are a number of examples in the gradescope documentation, but these are in general either quite brief and so don't have all of the best practises recommended you'd want for practical use (see https://gradescope-autograders.readthedocs.io/en/latest/best_practices/), or are very well developed and complex with lots of bells and whistles that can be too much when just getting going.

This is a Gradescope example which has the features of:
 - A rate limiter to limit the number of times per day students can submit attempts
 - (Essentially) all code encapsulated in try/catch statements so that errors are caught and 'nice' messages presented to students via the /autograder/results/results.json file.
 - Access to the network is turned off before student submissions are executed.
 - Access to computer resources are explictly set, to go above any resource limits imposed by the container.
 - Student code executed in a seperate process to seperate student code from the test wrapper (to avoid crashes).
 - Ability to test arbitrary code (so could be any language). The test wrapper is in Python, and ASSERT statements in Python are used to test what is correct, with these coming after arbitrary code in an OS shell has been run.

To run and/or edit (in brief):
------------------------------
 - Designed to work in the default gradescope Docker environment (currently Ubuntu 22.04 based).
 - All of the files in this folder should be zipped into a file called source.zip.
 - This zip file is what is uploaded to Gradescope

This Hellow World example expects a file called HelloWorld.c which, when compiled, displays "Hello World" to the output. There are two marks available, one for whether the code compiles and one for whether the correct output is displayed.

If wanting to modify, in principle you just need to edit the lines in test/tests_lab1.py:
 - command =
 - self.assertEqual
to run whatever tasks and tests that you want. 

Notes
-----
 - If editing in Windows that Unix style line endings are required for the gradescope system to run the files correctly. You may need to change a setting in your text editor to set the line ending style. 
 - The scipts used are not POSIX compliant. They assume bash and GNU date are present. (Which should be fine for any Linux based container.)

More info
--------- 
setup.sh runs first and is part of the set up process. It is run when the container is initialised, so is only run once. It installs the required components, and so anything that needs installing to the system should be done in here. This includes Python modules. Note that we use a hard coded Python 3.10. There's nothing too special about this particular version, it's just fixed to keep the Python stable, and >=3.9 is needed for subprocess to accept different users. All Python activities done in a virtual environment called venv, stored in /venv.

run_autograder.sh is called whenever a new student submission is received. This first makes 2 users: student which is for running the code, and tester which does anything else which touches the code. Other actions run as root. You could do basically everything as tester (see note on Python below) but I don't at the moment. This aims to be in-line with gradescope where setup runs as root, but anything interacting with the code is run as an unprivileged user. User student cannot see the test folder, and only root can write to the results folder. 

The student submission is put in /autograder/source/student_code which has write permissions so students can compile code. The actual submitted file has write permissions removed so students can't edit their own code post-submissions. Note that helper_functions includes scripts taken from elsewhere (https://www.xmodulo.com/catch-handle-errors-bash.html0 to give an error report to /autograder/results/results/results.json if anything goes wrong.
 
test_wrapper.py then sets up the Python test environment which uses the unittest framework. Actual tests are in the tests folder. test_wrapper.py is run as root rather than tester. Code is executed in a different process using subprocess, and run as user student with the user switch happening in the subprocess.Popen call. (It might be better to run test_wrapper.py as tester rather than root, but subprocess.Popen doesn't seem to then be able to switch the user. It might be possible to get this to work in the future.)

There's a number of more security suggestions in https://saligrama.io/blog/post/gradescope-autograder-security/
 but I haven't been over them yet.