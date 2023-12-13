Build: docker build -t "eeen10242_c_programming:latest" .
 
Run locally: docker run --rm -it -v /path/to/submission:/autograder/submission -v /path/to/results:/autograder/results eeen10242_c_programming:latest bash
 
 Based on examples at https://github.com/gradescope
 
 Note UNIX line endings
 
 setup.sh comes first and is part of the set up process. Run when the container is intialised, so is only run once. Installs the required components Anything the needs installing done in here. This includes Python modules
   Uses Python 3.10. Nothing too special about this particular version, just fixed the version to keep stable
   All Python activities done in a virtual environment called venv, stored in /venv
 
 run_autograder.sh is called whenever a new student submission is received. It makes a user called student and taks are run as this user. There's then one script to move the submission to the correct place (here /autograder/source/student_code). The main thing is getting the permissions correct, if things don't work it's often just that the file has the wrong permissions and so can't be seen. /autograder/source is 771 so students can execute the scripts there, but not read or write them in their own code. student_code is set to 775 so students can read and execute them (as part of the other permissions) but not write anything post-submission.
 
 helper_functions includes scipts taken from elsewhere https://www.xmodulo.com/catch-handle-errors-bash.html and 
 https://jqlang.github.io/jq/ to smooth the processing.
 
 The submmission is moved to student_code in bash with a try and catch, with JSON written by the jq function if an error occurs (indicating the wrong filename was present!).
 
 