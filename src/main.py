import events
import logging
import log
import traceback
import requests
from match import match_queue as mq

print("is ready", flush=True)
log.init()
logger=logging.getLogger("main")

while True:
    token=""
    try:
        print("Wating for new games ...", flush=True)
        match=mq.fetch()
        if not match:
            continue
        
        token=match.game_id
        # Check game is real!
        data = {
            "token": token
        }
        result = requests.get("https://api.aichallenge.ir/api/infra-gateway/game", params=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        if result.status_code == 404:
            print("///////////////////////// Skipping ////////////////////////////")
            continue
    
        print(f"game_id: {token}", flush=True)
        log.new_token_logger(token)
        events.push(events.Event(token=token, status_code=events.EventStatus.MATCH_STARTED.value,title='match started successfully!'))
        
        event_list = match.hold()
        logger.info(f"resulting events are:{len(event_list)}")
      
        events.push_all(event_list)
        mq.commit(match)
      
    except Exception as e:
        traceback.print_exc()
        logger.exception(f"an error accoured {e}")
    finally:
        log.remove_token_logger(token)
