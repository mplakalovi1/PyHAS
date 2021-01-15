import xml.etree.ElementTree as ET
import logging


class Parser:

    def __init__(self, mpd_file: str, mpdurl: str):
        self.myroot = ET.fromstring(mpd_file)  # parsing xml file from string
        self.mpdUrl = mpdurl
        self.namespace = None
        self.minBufferTime = None
        self.mediaPresentationDuration = None
        self.maxSegmentDuration = None
        self.segmentsNumber = None
        self.mpdTitle = None
        self.initialization = None
        self.media = dict()
        self.segments = dict()
        self.bandwidths = list()

    def simple(self):  # parsing simple .XML file
        self.namespace = self.myroot.tag.split("}")[0] + "}"  # extracting xmlns for proper search function

        minbuffertime = self.myroot.attrib['minBufferTime']  # reading minBufferTime in xml specific format
        mediapresentationduration = self.myroot.attrib['mediaPresentationDuration']  # reading mediaPresentationDuration in xml specific format
        maxsegmentduration = self.myroot.attrib['maxSegmentDuration']  # reading maxSegmentDuration in xml specific format

        self.minBufferTime = float(minbuffertime[minbuffertime.find('T') + 1: minbuffertime.find('S')])  # converting from string to float

        self.mediaPresentationDuration = float(mediapresentationduration[mediapresentationduration.find('T') + 1: mediapresentationduration.find('H')]) * 3600 + \
                                         float(mediapresentationduration[mediapresentationduration.find('H') + 1: mediapresentationduration.find('M')]) * 60 + \
                                         float(mediapresentationduration[mediapresentationduration.find('M') + 1: mediapresentationduration.find('S')])

        self.maxSegmentDuration = float(maxsegmentduration[maxsegmentduration.find('T') + 1: maxsegmentduration.find('H')]) * 3600 + \
                                  float(maxsegmentduration[maxsegmentduration.find('H') + 1: maxsegmentduration.find('M')]) * 60 + \
                                  float(maxsegmentduration[maxsegmentduration.find('M') + 1: maxsegmentduration.find('S')])

        self.segmentsNumber = int(self.mediaPresentationDuration/self.maxSegmentDuration + (self.mediaPresentationDuration % self.maxSegmentDuration > 0))
        self.mpdTitle = self.myroot.find(self.namespace + 'ProgramInformation').find(self.namespace + 'Title').text  # MPD file Title
        self.initialization = self.myroot.find(self.namespace + 'Period').find(self.namespace + 'AdaptationSet').find(self.namespace + 'SegmentTemplate').get('initialization')

        # segments representations:
        for representation in self.myroot.find(self.namespace + 'Period').find(self.namespace + 'AdaptationSet').iter(self.namespace + 'Representation'):
            self.segments['segment' + representation.attrib['id']] = representation.attrib
            self.media[representation.get('bandwidth')] = representation.find(self.namespace + 'SegmentTemplate').get('media')
            self.bandwidths.append(int(representation.get('bandwidth')))

        self.bandwidths.sort()  # bandwidths sorted in ascending order
        # Logging informations
        logging.info("MPD file informations:"
                     "\nMPD file title: {}"
                     "\nStream duration: {} seconds"
                     "\nSegment duration: {} seconds"
                     "\nSegments number: {}"
                     "\nRepresentations: {}".format(self.mpdTitle, self.mediaPresentationDuration, self.maxSegmentDuration, self.segmentsNumber, self.segments))

    @property
    def initialization_url(self):
        index = self.mpdUrl.rfind('/') + 1
        return self.mpdUrl[:index] + self.initialization

    def get_media_url(self, segment: float, number: float):
        index = self.mpdUrl.rfind('/') + 1
        return (self.mpdUrl[:index] + self.media[str(segment)]).replace('$Number$', str(number))
