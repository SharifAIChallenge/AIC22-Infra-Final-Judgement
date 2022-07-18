#!/bin/bash
# curl "https://raw.githubusercontent.com/SharifAIChallenge/final-judgment/master/resources/map.config" > /tmp/match/map.config
# curl "https://raw.githubusercontent.com/SharifAIChallenge/AIC21-Minigame/main/map.config" > /tmp/match/map.config
curl "https://raw.githubusercontent.com/SharifAIChallenge/AIC21-Game/main/mini_server/map.config" > /tmp/match/map.config
(cd /tmp/match && java -jar /usr/local/match/match.jar $@)
