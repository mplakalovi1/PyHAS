import HTTP
import PARSER


mpd_file = HTTP.Http('http://ftp.itec.aau.at/datasets/DASHDataset2014/BigBuckBunny/4sec/BigBuckBunny_4s_simple_2014_05_09.mpd')
# print(mpd_file.getcontent())
# print(mpd_file.successful())
# print(mpd_file.getsize(), mpd_file.getrsptime())
# print(mpd_file.usersbandwidth())
# print(mpd_file.response.status_code)
# print(mpd_file.successful())

parsed_mpd = PARSER.Parser(mpd_file.getcontent())  # instance of Parser class
parsed_mpd.bigbuckbunny_4s_simple()  # parsing BigBuckBunny_4s_simple .XML file
# print(parsed_mpd.__dict__)