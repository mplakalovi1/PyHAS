import HTTP
import xmlparser
import algorithm
import logging
from requests import exceptions
import sys
from configparser import ConfigParser
import time

start = time.time()
# reading configuration: ----------------------------------------------
config = ConfigParser()
config.read('config.ini')

mpd_url: str = config['mpd file']['mpd']
algorithm_to_use: str = config['sensitive_informations']['algorithm']
segments_num: int = int(config['sensitive_informations']['segments_number'])
timeout: int = int(config['sensitive_informations']['timeout'])
buffer_threshold: int = int(config['sensitive_informations']['buffer_threshold'])
buffer_filling: int = int(config['sensitive_informations']['buffer_filling'])
# ---------------------------------------------------------------------


# function with try except statement for sending HTTP requests: ---------------------------
def try_req_exc(url):
    global timeout_counter
    try:
        r = HTTP.Http(url, timeout)  # send request
        r.raise_for_status()  # raise HTTPError, if one occurred
        timeout_counter = 0  # restarting timeout_counter for next request
        return r
    except exceptions.HTTPError as err1:
        logging.error(str(err1))
        sys.exit()
    except exceptions.ConnectionError as err2:
        logging.error(str(err2))
        sys.exit()
    except exceptions.Timeout as err3:
        timeout_counter += 1
        logging.error(str(err3))
        if timeout_counter == 3:  # after 3 successive timeouts end streaming ! <----------
            sys.exit()
        return try_req_exc(url)
    except exceptions.RequestException as err4:
        logging.error(str(err4))
        sys.exit()
# -----------------------------------------------------------------------------------------


timeout_counter = 0
# Sending request for .MPD file:
mpd_response = try_req_exc(mpd_url)
# Parsing mpd_response:
mpd_file = xmlparser.Parser(mpd_response.content, mpd_url)  # instance of xmlparser class
mpd_file.simple()  # parsing .MPD file

# Checking if number of segments assigned by configuration matches max number of segments:
if segments_num > mpd_file.segments_number:  # <------ if assigned number of segments exceed max number of segments
    segments_num = mpd_file.segments_number

# Deciding which algorithm to be used:
if algorithm_to_use == 'Algorithm1':
    algorithm = algorithm.Algorithm1(mpd_file.bitrates)
elif algorithm_to_use == 'Algorithm2':
    algorithm = algorithm.Algorithm2(mpd_file.bitrates)
else:
    logging.info("Algorithm given by the configuration is not defined")
    sys.exit()

# Sending request for initialization .MP4 file
initialization_file = try_req_exc(mpd_file.get_initialization_url())

# Sending requests for segments: -------------------------------------------------------------------------------------
segments_counter = 1
logging.info("Filling buffer with {} seconds !".format(buffer_filling * mpd_file.segment_duration))
while segments_counter <= segments_num:
    if algorithm.buffer > buffer_threshold:
        logging.info("BUFFER THRESHOLD REACHED ! ({} seconds)".format(algorithm.buffer))
        time.sleep(mpd_file.segment_duration)
        algorithm.buffer -= mpd_file.segment_duration

    if segments_counter <= buffer_filling:  # <------ filling buffer
        logging.info("Segment number {}: ".format(segments_counter))
        segment = try_req_exc(mpd_file.get_media_url(algorithm.bitrates[0], segments_counter))
        # Logging: --------------------------------------------------------------
        logging.info("Response size: {} bytes".format(segment.size))
        logging.info("Response time: {} seconds".format(segment.response_time))
        logging.info("User's bandwidth: {} bps".format(segment.users_bandwidth))
        # -----------------------------------------------------------------------
        algorithm.usersbandwidth = segment.users_bandwidth
        algorithm.previous = algorithm.bitrates[0]
        algorithm.buffer += mpd_file.segment_duration
    else:  # started streaming
        if segments_counter == buffer_filling + 1:
            logging.info("STREAMING STARTED !")

        logging.info("Segment number {}: ".format(segments_counter))
        algorithm.alg()  # <------ ALGORITHM called!
        segment = try_req_exc(mpd_file.get_media_url(algorithm.previous[-1], segments_counter))
        # Logging: --------------------------------------------------------------
        logging.info("Response size: {} bytes".format(segment.size))
        logging.info("Response time: {} seconds".format(segment.response_time))
        logging.info("User's bandwidth: {} bps".format(segment.users_bandwidth))
        # -----------------------------------------------------------------------
        algorithm.usersbandwidth = segment.users_bandwidth
        algorithm.buffer += mpd_file.segment_duration - (timeout_counter * timeout + segment.response_time)

    segments_counter += 1
# --------------------------------------------------------------------------------------------------------------------

logging.info("{} SEGMENTS DOWNLOADED !".format(segments_num))
logging.info("Stats: "
             "\nUser's bandwidth through streaming [bps]: {}"
             "\nRequested bit rates through streaming [bps]: {}".format(algorithm.usersbandwidth, algorithm.previous))
