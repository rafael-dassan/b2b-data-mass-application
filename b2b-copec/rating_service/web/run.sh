#!/bin/bash
ARRAY=(bavaria mitiendacn backus)
rm -r ./results/*

for i in "${ARRAY[@]}"
do
    echo "Starting $i scenarios"
    FILE=five_stars_scenarios_$i
    robot -d ./results ./tests/$FILE.robot
    mkdir -p ./results/$FILE
    mv ./results/*.* ./results/$FILE

    FILE=two_star_scenarios_$i
    robot -d ./results ./tests/$FILE.robot
    mkdir -p ./results/$FILE
    mv ./results/*.* ./results/$FILE

    FILE=one_star_scenarios_$i
    robot -d ./results ./tests/$FILE.robot
    mkdir -p ./results/$FILE
    mv ./results/*.* ./results/$FILE

    # FILE=single_account_scenarios_$i
    # robot -d ./results ./tests/$FILE.robot
    # mkdir -p ./results/$FILE
    # mv ./results/*.* ./results/$FILE

    echo "$i scenarios finished"
done