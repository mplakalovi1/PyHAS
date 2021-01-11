import HTTP
import PARSER
import algorithm
import logging
from requests import exceptions
import sys

TIMEOUT = 5


def try_req_exc(url):
    try:
        r = HTTP.Http(url)  # send request
        r.response.raise_for_status()  # raise HTTPError, if one occurred
        return r
    except exceptions.HTTPError as err1:
        logging.error(str(err1) + " error1")
        sys.exit()
    except exceptions.ConnectionError as err2:
        logging.error(str(err2) + " error2")
        sys.exit()
    except exceptions.Timeout as err3:
        timeout_counter[0] += 1
        logging.error(str(err3) + " error3")
        if timeout_counter[0] == 3:  # after 3 successive timeouts end streaming ! <----------
            return
        try_req_exc(url)
    except exceptions.RequestException as err4:
        logging.error(str(err4) + " error4")
        sys.exit()


# ---------------------------------------------------------------------------------------------------------------------
# Streams:
mpd_url = {
    'BigBuckBunny_4s_simple': 'http://ftp.itec.aau.at/datasets/DASHDataset2014/BigBuckBunny/4sec'
                              '/BigBuckBunny_4s_simple_2014_05_09.mpd',
    'ElephantsDream_4s_simple': 'http://ftp.itec.aau.at/datasets/DASHDataset2014/ElephantsDream/4sec'
                                '/ElephantsDream_4s_simple_2014_05_09.mpd',
    'OfForestAndMen_4s_simple': 'http://ftp.itec.aau.at/datasets/DASHDataset2014/OfForestAndMen/4sec'
                                '/OfForestAndMen_4s_simple_2014_05_09.mpd',
    'TearsOfSteel_4s_simple': 'http://ftp.itec.aau.at/datasets/DASHDataset2014/TearsOfSteel/4sec'
                              '/TearsOfSteel_4s_simple_2014_05_09.mpd'}
segment_counter = 1
buffer = 0

timeout_counter = [0]
# Sending request for .MPD file
mpd_file = try_req_exc(mpd_url['BigBuckBunny_4s_simple'])  # requesting .MPD for BigBuckBunny_4s
parsed_mpd = PARSER.Parser(mpd_file.getcontent(), mpd_url['BigBuckBunny_4s_simple'])  # instance of Parser class
parsed_mpd.simple()  # parsed .MPD file

timeout_counter[0] = 0  # restarting timeout counter before sending next request
logging.info("STREAM STARTED!")
# Sending request for .mp4 initialization
initialization = try_req_exc(parsed_mpd.initialization_url())

alg = algorithm.Algorithm(parsed_mpd.bandwidths)  # instance of Algorithm class

# Sending requests for segments using algorithm1:
# while segment_counter <= parsed_mpd.segmentsNumber:
#     if segment_counter == 1:  # first segment of minimum quality
#         logging.info("Segment number {}: ".format(segment_counter))
#         timeout_counter[0] = 0  # restarting timeout counter before sending next request
#         segment = try_req_exc(parsed_mpd.media_url(parsed_mpd.bandwidths[0], segment_counter))
#         logging.info("Response size: {} bytes".format(segment.getsize()))
#         logging.info("Response time: {} seconds".format(segment.getrsptime()))
#         logging.info("User's bandwidth: {} bps".format(segment.usersbandwidth()))
#         buffer += 4
#         logging.info("Buffer = {} sec".format(buffer))
#
#     elif segment_counter == 2:  # second segment of minimum quality
#         logging.info("Segment number {}: ".format(segment_counter))
#         timeout_counter[0] = 0  # restarting timeout counter before sending next request
#         segment = try_req_exc(parsed_mpd.media_url(parsed_mpd.bandwidths[0], segment_counter))
#         logging.info("Response size: {} bytes".format(segment.getsize()))
#         logging.info("Response time: {} seconds".format(segment.getrsptime()))
#         logging.info("User's bandwidth: {} bps".format(segment.usersbandwidth()))
#         buffer = buffer + 4 - (timeout_counter[0] * TIMEOUT + segment.getrsptime())
#         if buffer < 0:
#             buffer = 0
#             logging.info("BUFFER STALLED ( Buffer = {} sec ) !".format(buffer))
#         else:
#             logging.info("Buffer = {} sec".format(buffer))
#
#     else:  # algorithm makes decision about next segments
#         logging.info("Segment number {}: ".format(segment_counter))
#         timeout_counter[0] = 0  # restarting timeout counter before sending next request
#         segment = try_req_exc(parsed_mpd.media_url(alg.algorithm_1(segment.usersbandwidth()), segment_counter))
#         logging.info("Response size: {} bytes".format(segment.getsize()))
#         logging.info("Response time: {} seconds".format(segment.getrsptime()))
#         logging.info("User's bandwidth: {} bps".format(segment.usersbandwidth()))
#         buffer = buffer + 4 - (timeout_counter[0] * TIMEOUT + segment.getrsptime())
#         if buffer < 0:
#             buffer = 0
#             logging.info("BUFFER STALLED ( Buffer = {} sec ) !".format(buffer))
#         else:
#             logging.info("Buffer = {} sec".format(buffer))
#
#     segment_counter += 1
# # ---------------------------------------------------------------------------------------------------------------
# logging.info("STREAM FINISHED!")

# Sending requests for segments using algorithm2:
while segment_counter <= parsed_mpd.segmentsNumber:
    if segment_counter == 1:  # first segment of minimum quality
        logging.info("Segment number {}: ".format(segment_counter))
        timeout_counter[0] = 0  # restarting timeout counter before sending next request
        segment = try_req_exc(parsed_mpd.media_url(parsed_mpd.bandwidths[0], segment_counter))
        logging.info("Response size: {} bytes".format(segment.getsize()))
        logging.info("Response time: {} seconds".format(segment.getrsptime()))
        logging.info("User's bandwidth: {} bps".format(segment.usersbandwidth()))
        buffer += 4
        logging.info("Buffer = {} sec".format(buffer))

    elif segment_counter == 2:  # second segment of minimum quality
        logging.info("Segment number {}: ".format(segment_counter))
        timeout_counter[0] = 0  # restarting timeout counter before sending next request
        bandwidth = parsed_mpd.bandwidths[0]
        segment = try_req_exc(parsed_mpd.media_url(bandwidth, segment_counter))
        logging.info("Response size: {} bytes".format(segment.getsize()))
        logging.info("Response time: {} seconds".format(segment.getrsptime()))
        logging.info("User's bandwidth: {} bps".format(segment.usersbandwidth()))
        buffer = buffer + 4 - (timeout_counter[0] * TIMEOUT + segment.getrsptime())
        if buffer < 0:
            buffer = 0
            logging.info("BUFFER STALLED ( Buffer = {} sec ) !".format(buffer))
        else:
            logging.info("Buffer = {} sec".format(buffer))

    else:  # algorithm makes decision about next segments
        logging.info("Segment number {}: ".format(segment_counter))
        timeout_counter[0] = 0  # restarting timeout counter before sending next request
        bandwidth = alg.algorithm_2(segment.usersbandwidth(), bandwidth)
        segment = try_req_exc(parsed_mpd.media_url(bandwidth, segment_counter))
        logging.info("Response size: {} bytes".format(segment.getsize()))
        logging.info("Response time: {} seconds".format(segment.getrsptime()))
        logging.info("User's bandwidth: {} bps".format(segment.usersbandwidth()))
        buffer = buffer + 4 - (timeout_counter[0] * TIMEOUT + segment.getrsptime())
        if buffer < 0:
            buffer = 0
            logging.info("BUFFER STALLED ( Buffer = {} sec ) !".format(buffer))
        else:
            logging.info("Buffer = {} sec".format(buffer))

    segment_counter += 1
# ---------------------------------------------------------------------------------------------------------------
logging.info("STREAM FINISHED!")
