#!/usr/bin/env bash
# Note that this uses the GNU date command which isn't POSIX compliant. It should work fine on any modern Linux distrubtion, but may not work on macOS and similar


# Set the number of submissions allowed per unit time
NUMBER_LIMIT=24
UNIT_TIME="1 day"


# Gradescope saves timestamps in a string as "2023-12-06T03:07:35.807958-08:00". Function to convert this to date friendly format 2023/12/06 03:07:35.807958 -08:00
convert_json_date_to_bash_date () {
	local converted_date=$(sed "s/T/ /" <<< "$1")
    local converted_date=$(sed "s/-{3}/\//" <<< "$converted_date")
    local converted_date=$(sed "s/\"//g" <<< "$converted_date")
	local output_date=$(date --date="$converted_date")
    echo "$output_date"
}


# Get the date of the current submission from submission_metadata.json
submission_date_json=$(jq '.created_at' /autograder/submission_metadata.json)
submission_date_bash="$(convert_json_date_to_bash_date "$submission_date_json")"


# Find 1 UNIT_TIME earlier for the counting period over which submissions are limited.
one_day_earlier_bash=$(date --date="$submission_date_bash - $UNIT_TIME")


# Get the list of previous submissions from submission_metadata.json and put into an array
previous_submission_dates_json=$(jq .previous_submissions[].submission_time /autograder/submission_metadata.json)
readarray -t array_of_dates <<< "$previous_submission_dates_json"
#echo "${array_of_dates[@]}"


# Iterate through the previous submissions, looking at the $NUMBER_LIMIT last ones in the array only as only these affect the decision
for i in ${array_of_dates[@]: $((-1*"$NUMBER_LIMIT"))}; do
    converted_date="$(convert_json_date_to_bash_date "$i")"
	if [[ "$one_day_earlier_bash" < "$converted_date" ]];  then
    	((var++)) # var is the count of number of submissions in the period
    fi  
	previous_submission_dates_bash+=( "$converted_date")
done


# Check whether the daily limit has been execced and output an error if so. The error message is just put to stdout, to be captured by a script that calls this one. This allows runtime errors to be put on stderr and captured seperately
if [[ "$var" -ge "$NUMBER_LIMIT" ]]; then
   new_date_bash=$(date --date="${previous_submission_dates_bash[0]} + $UNIT_TIME + 1 second")
   echo "ERROR: We only allow people to make" $NUMBER_LIMIT "submissions each day, and you have exceeded this limit. You need to wait until" $new_date_bash "before you can submit again."
fi