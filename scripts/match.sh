#!/bin/bash
#curl "https://raw.githubusercontent.com/SharifAIChallenge/final-judgment/master/resources/map.config" > /tmp/match/map.config
(cd /tmp/match && java -jar /usr/local/match/match.jar $@)
