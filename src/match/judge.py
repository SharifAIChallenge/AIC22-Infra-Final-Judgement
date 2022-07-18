from subprocess import STDOUT, check_output, TimeoutExpired,CalledProcessError
from match.minio_cli import MinioClient 
from events import Event, EventStatus
import logging
import subprocess
import json
import os
import stat


logger=logging.getLogger("judge")



STATS_KEYNAME = "stats"

match_base_dir="/tmp/match"
match_record_path = f"{match_base_dir}/log.json"
match_log_path = f"{match_base_dir}/Log/server/server.log"
match_timeout= int(os.getenv("MATCH_TIMEOUT"))
match_runcommand=["match", "--first-team=/etc/spawn/1", "--second-team=/etc/spawn/2", "--read-map=map"]

def download_code(code_id, dest) -> bool:
    logger.info(f"start processing code [{code_id}]")
    try:
        zip_file = MinioClient.get_compiled_code(code_id)
        if zip_file is None:
            return False

        # remove previous binary by force!!!!
        os.system('rm -rf binary')
        logger.info("removed previous binary")

        # unzip source binary
        with open('code.tgz', 'wb') as f:
            f.write(zip_file)
        if os.system("tar -xvzf code.tgz")!=0:
            return False
        logger.info(f"successfuly unziped binary [{code_id}]")
        
        # move binary to given dest
        os.rename('binary',dest);
        logger.info(f"successfuly moved binary [{code_id}] to [{dest}]")
        
        # give execute permission to new binary
        os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)
        logger.info(f"[{dest}] is now executable")
        
        # cleanup the code.tgz file
        os.remove("code.tgz")
    except:
        return False
    return True


def download_map(map_id, dest) -> bool:
    zip_file = MinioClient.get_map(map_id)
    if zip_file is None:
        return False

    with open(dest, 'wb') as f:
        f.write(zip_file)
    
    logger.info(f"map is stored to [{dest}] successfuly")
    return True
    


def __judge() -> int:

    try:
        logger.info("match started")
        output = check_output(match_runcommand, stderr=STDOUT, timeout=match_timeout)
        logger.info("match held successfully")
    except TimeoutExpired:
        logger.warning("match timeout exiceded!")
        return -2
    except CalledProcessError:
        logger.warning("match returned none zero exitcode!")
        return -1
    finally:
        # just to make sure every client is dead
        os.system("kill -9 `ps -aux | grep spawn | awk '{print$2}'`")
        
    logger.debug(output)
    return 0

def new_isol_area():
    try:
        os.mkdir(match_base_dir)
    except FileExistsError:
        os.system(f"rm -rf {match_base_dir}")
        logger.warning("directory already existed, removing it...")
        os.mkdir(match_base_dir)
    logger.info(f"new isolated area is creaed in [{match_base_dir}]")

def rm_isol_area():
    os.system(f"rm -rf {match_base_dir}")

    # delete all temprory shitty pyinstaller files
    # TODO: find a better way later
    os.system("rm -rf /tmp/_*")
    logger.info(f"isolated area is removed")


def judge(players, map_id, game_id) -> [Event]:
    resulting_events = []

    # make an isolate area
    new_isol_area()
        
    # downloading players code
    for index, player in enumerate(players):
        if not download_code(player, f"/etc/spawn/{index+1}"):
            resulting_events.append(Event(token=player, status_code=EventStatus.FILE_NOT_FOUND.value,
                         title='failed to fetch the compiled code!'))
            resulting_events.append(Event(token=game_id, status_code=EventStatus.MATCH_NOT_PROVIDED.value,
                         title='failed to fetch clients code!'))

            return resulting_events

    # download map
    if not download_map(map_id, f"{match_base_dir}/map"):
        resulting_events.append(Event(token=map_id, status_code=EventStatus.FILE_NOT_FOUND.value,
                     title='failed to fetch the map!'))
        resulting_events.append(Event(token=game_id, status_code=EventStatus.MATCH_NOT_PROVIDED.value,
                         title='failed to fetch the map!'))
        return resulting_events

    # run match
    exit_code=__judge()
    try:
        # extract the match stats      
        stats = str(json.load(open(match_record_path))[STATS_KEYNAME])
    except:
        stats = ""
        logger.warning("failed fo fetch match stats")
    
    if exit_code == -1:
        resulting_events.append(Event(token=game_id, status_code=EventStatus.MATCH_FAILED.value,
                                title='failed to hold the match', message_body=stats))
    elif exit_code == -2:
        resulting_events.append(Event(token=game_id, status_code=EventStatus.MATCH_TIMEOUT.value,
                                title='match timeout exceeded', message_body=stats))   
    elif exit_code == 0:
        resulting_events.append(Event(token=game_id, status_code=EventStatus.MATCH_SUCCESS.value,
                 title='match finished successfully!', message_body=stats))
    

    # used for uploading clients logs if needed
    # for player in players:
    #     with open(f'{player_name[player]}.log', 'rb') as file:
    #         if not MinioClient.upload_logs(path=game_id, file=file, file_name=player):
    #             return Event(token=player, status_code=EventStatus.UPLOAD_FAILED.value,
    #                          title='failed to upload the player log!')

    # upload game log
    try:
        # zip the file
        os.system(f"(cd `dirname {match_record_path}` && tar -cvzf  temp.tgz `basename {match_record_path}` && mv temp.tgz `basename {match_record_path}`)")
        # upload
        with open(match_record_path, 'rb') as file:
            if not MinioClient.upload_logs(path=game_id, file=file, file_name=game_id):
                resulting_events.append(Event(token=game_id, status_code=EventStatus.UPLOAD_FAILED.value,
                            title='failed to upload the game log!'))
    except:
        logger.warning(f"file {match_record_path} didnt exist!")
   
    # upload server log
    with open(match_log_path, 'rb') as file:
        if not MinioClient.upload_logs(path=game_id, file=file, file_name=f'{game_id}.out'):
            resulting_events.append(Event(token=game_id, status_code=EventStatus.UPLOAD_FAILED.value,
                        title='failed to upload the game server output!'))


    # clean up
    rm_isol_area()

    return resulting_events
