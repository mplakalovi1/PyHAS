import xml.etree.ElementTree as ET
import logging


class Parser:

    def __init__(self, mpd_file: str, mpdurl: str):
        self.__myroot = ET.fromstring(mpd_file)  # parsing xml file from string
        self.__mpdUrl = mpdurl
        self.__namespace = None
        self.__minBufferTime = None
        self.__mediaPresentationDuration = None
        self.__maxSegmentDuration = None
        self.__segmentsNumber = None
        self.__mpdTitle = None
        self.__initialization = None
        self.__media = dict()
        self.__segments = dict()
        self.__bitrates = list()

    def simple(self):  # parsing simple .XML file
        self.__namespace = self.__myroot.tag.split("}")[0] + "}"  # extracting xmlns for proper search function

        minbuffertime = self.__myroot.attrib['minBufferTime']  # reading minBufferTime in xml specific format
        mediapresentationduration = self.__myroot.attrib['mediaPresentationDuration']  # reading mediaPresentationDuration in xml specific format
        maxsegmentduration = self.__myroot.attrib['maxSegmentDuration']  # reading maxSegmentDuration in xml specific format

        self.__minBufferTime = float(minbuffertime[minbuffertime.find('T') + 1: minbuffertime.find('S')])  # converting from string to float

        self.__mediaPresentationDuration = float(mediapresentationduration[mediapresentationduration.find('T') + 1: mediapresentationduration.find('H')]) * 3600 + \
                                           float(mediapresentationduration[mediapresentationduration.find('H') + 1: mediapresentationduration.find('M')]) * 60 + \
                                           float(mediapresentationduration[mediapresentationduration.find('M') + 1: mediapresentationduration.find('S')])

        self.__maxSegmentDuration = float(maxsegmentduration[maxsegmentduration.find('T') + 1: maxsegmentduration.find('H')]) * 3600 + \
                                    float(maxsegmentduration[maxsegmentduration.find('H') + 1: maxsegmentduration.find('M')]) * 60 + \
                                    float(maxsegmentduration[maxsegmentduration.find('M') + 1: maxsegmentduration.find('S')])

        self.__segmentsNumber = int(self.__mediaPresentationDuration / self.__maxSegmentDuration + (self.__mediaPresentationDuration % self.__maxSegmentDuration > 0))
        self.__mpdTitle = self.__myroot.find(self.__namespace + 'ProgramInformation').find(self.__namespace + 'Title').text  # MPD file Title
        self.__initialization = self.__myroot.find(self.__namespace + 'Period').find(self.__namespace + 'AdaptationSet').find(self.__namespace + 'SegmentTemplate').get('initialization')

        # __segments representations:
        for representation in self.__myroot.find(self.__namespace + 'Period').find(self.__namespace + 'AdaptationSet').iter(self.__namespace + 'Representation'):
            self.__segments['segment' + representation.attrib['id']] = representation.attrib
            self.__media[representation.get('bandwidth')] = representation.find(self.__namespace + 'SegmentTemplate').get('media')
            self.__bitrates.append(int(representation.get('bandwidth')))

        self.__bitrates.sort()  # bitrates sorted in ascending order
        # Logging informations
        logging.info("MPD file informations:"
                     "\nMPD file title: {}"
                     "\nStream duration: {} seconds"
                     "\nSegment duration: {} seconds"
                     "\nSegments number: {}"
                     "\nRepresentations: {}".format(self.__mpdTitle, self.__mediaPresentationDuration, self.__maxSegmentDuration, self.__segmentsNumber, self.__segments))

    @property
    def segments_number(self):
        return self.__segmentsNumber

    @property
    def bitrates(self):
        return self.__bitrates

    @property
    def segment_duration(self):
        return self.__maxSegmentDuration

    def get_initialization_url(self):
        index = self.__mpdUrl.rfind('/') + 1
        return self.__mpdUrl[:index] + self.__initialization

    def get_media_url(self, segment: int, number: int):
        index = self.__mpdUrl.rfind('/') + 1
        return (self.__mpdUrl[:index] + self.__media[str(segment)]).replace('$Number$', str(number))


