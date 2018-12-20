#!/bin/bash

rm -r ./results/*

######### FIVE SCENARIOS
FILE=five_stars_scenarios_bavaria
robot -d ./results ./tests/$FILE.robot
mkdir -p ./results/$FILE
mv ./results/*.* ./results/$FILE

#FILE=five_stars_scenarios_bavaria
#robot -d ./results ./tests/$FILE.robot
#mkdir -p ./results/$FILE
#mv ./results/*.* ./results/$FILE

######### TWO SCENARIOS
FILE=two_star_scenarios_bavaria
robot -d ./results ./tests/$FILE.robot
mkdir -p ./results/$FILE
mv ./results/*.* ./results/$FILE

#FILE=two_star_scenarios_bavaria
#robot -d ./results ./tests/$FILE.robot
#mkdir -p ./results/$FILE
#mv ./results/*.* ./results/$FILE

######### ONE SCENARIOS
FILE=one_star_scenarios_bavaria
robot -d ./results ./tests/$FILE.robot
mkdir -p ./results/$FILE
mv ./results/*.* ./results/$FILE
#
# FILE=single_account_scenarios_backus
# robot -d ./results ./tests/$FILE.robot
# mkdir -p ./results/$FILE
# mv ./results/*.* ./results/$FILE
#
#FILE=one_star_scenarios_bavaria
#robot -d ./results ./tests/$FILE.robot
#mkdir -p ./results/$FILE
#mv ./results/*.* ./results/$FILE
#
######### NON DISPLAY SCENARIOS
#FILE=non_display_rating_service_bavaria
#robot -d ./results ./tests/$FILE.robot
#mkdir -p ./results/$FILE
#mv ./results/*.* ./results/$FILE
#
#FILE=non_display_rating_service_bavaria
#robot -d ./results ./tests/$FILE.robot
#mkdir -p ./results/$FILE
#mv ./results/*.* ./results/$FILE
#
#FILE=non_display_rating_service_bavaria
#robot -d ./results ./tests/$FILE.robot
#mkdir -p ./results/$FILE
#mv ./results/*.* ./results/$FILE