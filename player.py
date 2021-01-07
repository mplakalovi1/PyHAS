import HTTP

mpd_file = HTTP.Http('http://ftp.itec.aau.at/datasets/DASHDataset2014/BigBuckBunny/4sec/BigBuckBunny_4s_simple_2014_05_09.mpd')
print(mpd_file.getcontent())
print(mpd_file.response.status_code)
print(mpd_file.successful())