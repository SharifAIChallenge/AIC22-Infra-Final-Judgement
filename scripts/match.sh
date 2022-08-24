#!/bin/bash
#curl "https://raw.githubusercontent.com/SharifAIChallenge/final-judgment/master/resources/map.config" > /tmp/match/map.config
export movementLogThresholdTimeMillisecond=1500
export clientReadinessThresholdTimeMillisecond=60000
export magicTurnTime=2000
(cd /tmp/match && movementLogThresholdTimeMillisecond=1500 clientReadinessThresholdTimeMillisecond=60000 magicTurnTime=2000 java -jar /usr/local/match/match.jar $@)
