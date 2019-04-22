#!/bin/bash

# Gets the time when the script has started
startTime=$(date +%s);

# App package name
package_name=$1

# Constants
DATE=$(date +'%d-%m-%Y_%T')

# Start monkey test
# Params:
# - throttle: delay between events
# - ignore-crashes: continue testing even after crashing
# - ignore-timeouts: ignore freeze
# - pct-touch: percentage of events that will be "touch"
# - last param: number of events
adb shell monkey -p ${package_name} --throttle 1000 --pct-touch 40 --ignore-crashes --ignore-timeouts 250 | adb logcat -d *:E > ${DATE}.txt

crash_number=$(cat ${DATE}.txt | grep "FATAL EXCEPTION" | wc -l)

if [ $crash_number = 0 ]
then
    mv ${DATE}.txt NOCRASH_${DATE}.txt
fi

printf "\n|----------OUTPUT-----------|"

printf "\nCrashes: %s" ${crash_number}

# Gets the time when the script has ended
endTime=$(date +%s);

# Calculates the execution time in seconds and prints
totalTime=$(($endTime-$startTime));
printf "\nTime elapsed: %s seconds\n" ${totalTime}

