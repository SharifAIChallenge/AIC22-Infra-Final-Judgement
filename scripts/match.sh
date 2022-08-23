#!/bin/bash
#curl "https://raw.githubusercontent.com/SharifAIChallenge/final-judgment/master/resources/map.config" > /tmp/match/map.config
(cd /tmp/match && movementLogThresholdTimeMillisecond=1500 clientReadinessThresholdTimeMillisecond=60000 java -jar /usr/local/match/match.jar $@)
