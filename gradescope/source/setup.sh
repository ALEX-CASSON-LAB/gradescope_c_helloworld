#!/usr/bin/env bash
# Assumes is run as root in / 

# Slight tidy-up for the installation
apt-get install -y apt-utils

# Install Python requirements
# - wheel for subprocess32 can run as a non-root users
# - subprocess32 so can run student code in a seperate process (so if it crashes the main process keeps going and can report back)
# - pyseccomp for securing the setup (e.g. removing network access)
# - gradescope-utils to give gradescope's tools to help the seup
apt-get install -y python3.10 python3.10-venv python3-pip
python3.10 -m venv venv
source /venv/bin/activate
python3.10 -m pip install wheel # has to be before subproces32 and in a seperate command so wheel install is complete first
python3.10 -m pip install subprocess32 pyseccomp gradescope-utils
deactivate

# Install gcc and similar for working with C
apt-get install -y build-essential

# Install jq for bash processing of JSON
apt-get install -y jq