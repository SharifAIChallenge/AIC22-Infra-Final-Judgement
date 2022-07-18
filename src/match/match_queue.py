from confluent_kafka import Consumer
from os import getenv
import logging
import json
from socket import gethostname

from match.match import Match

logger=logging.getLogger("match_queue")

KAFKA_ENDPOINT = getenv('KAFKA_ENDPOINT')
KAFKA_TOPIC_CONSUMER_GROUP = getenv('KAFKA_TOPIC_CONSUMER_GROUP')
KAFKA_TOPIC_MATCH = getenv('KAFKA_TOPIC_MATCH')


match_consumer = Consumer({
    'bootstrap.servers': KAFKA_ENDPOINT,
    'group.id': KAFKA_TOPIC_CONSUMER_GROUP,
    'auto.offset.reset': 'latest',
    'enable.auto.offset.store':False,
    'client.id': f'{gethostname()}',
    'enable.auto.commit': False,
    'session.timeout.ms': 10*1000,      #10 seconds
    'max.poll.interval.ms': 30*60*1000,  #30 minutes
    'heartbeat.interval.ms': 1*1000     #1 seconds
})
match_consumer.subscribe([KAFKA_TOPIC_MATCH])


fetched=[]

def fetch() -> Match:
    msg = match_consumer.poll()

    if msg is None:
        return None
    if msg.error():
        logger.error(f"error acurred while fetching new message: {msg.error()}")
        return None
    
    try:
        command = json.loads(msg.value().decode('utf-8'))
        logger.info(f"match is :{command}")
        
        m=Match(game_id=command['game_id'],map_id=command['map_id'],player_ids=command['player_ids'])
        fetched.append((m.game_id,msg))
        return m
    except:
        logger.warning(f"recived malformed message [{msg}]")
        logger.warning("ignoring...")
        match_consumer.commit(message=msg)
        return None

def __get_message(match):
    index=[i for i,m in enumerate(fetched) if m[0]==match.game_id][0]
    return fetched.pop(index)[1]

def commit(match):
    msg=__get_message(match)
    match_consumer.store_offsets(message=msg)
    match_consumer.commit(message=msg)
    logger.info("match was commited successfully!")


def close():
    match_consumer.close()

