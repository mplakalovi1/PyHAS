import xml.etree.ElementTree as ET
import logging


class Parser:
    def __init__(self, mpd_file):
        self.myroot = ET.fromstring(mpd_file)  # parsing xml file from string
        self.namespace = None
        self.minBufferTime = None
        self.mediaPresentationDuration = None
        self.segmentsNumber = None
        self.mpdTitle = None
        self.media = None
        self.initialization = None
        self.segments = dict()
        self.bandwidths = list()

    def bigbuckbunny_4s_simple(self):  # parsing BigBuckBunny_4s_simple .XML file
        self.namespace = self.myroot.tag.split("}")[0] + "}"  # extracting xmlns for proper search function

        minbuffertime = self.myroot.attrib['minBufferTime']  # reading minBufferTime in xml specific format
        mediapresentationduration = self.myroot.attrib['mediaPresentationDuration']  # reading mediaPresentationDuration in xml specific format

        self.minBufferTime = float(minbuffertime[minbuffertime.find('T') + 1: minbuffertime.find('S')])  # converting from string to float
        self.mediaPresentationDuration = float(mediapresentationduration[mediapresentationduration.find('T') + 1: mediapresentationduration.find('H')]) * 3600 + \
                                         float(mediapresentationduration[mediapresentationduration.find('H') + 1: mediapresentationduration.find('M')]) * 60 + \
                                         float(mediapresentationduration[mediapresentationduration.find('M') + 1: mediapresentationduration.find('S')])

        self.segmentsNumber = int(self.mediaPresentationDuration/4 + (self.mediaPresentationDuration % 4 > 0))
        self.mpdTitle = self.myroot.find(self.namespace + 'ProgramInformation').find(self.namespace + 'Title').text  # MPD file Title

        segmenttemplate = self.myroot.find(self.namespace + 'Period').find(self.namespace + 'AdaptationSet').find(self.namespace + 'SegmentTemplate').attrib
        self.media = segmenttemplate['media']
        self.initialization = segmenttemplate['initialization']

        # segments representations:
        i = 1
        for representation in self.myroot.iter(self.namespace + 'Representation'):
            self.segments['segment' + str(i)] = representation.attrib
            self.bandwidths.append(representation.get('bandwidth'))
            i += 1

        # Logging informations
        logging.info("MPD file informations:"
                     "\nMPD file title: {}"
                     "\nStream duration: {} seconds"
                     "\nSegments number: {}"
                     "\nRepresentations: {}".format(self.mpdTitle, self.mediaPresentationDuration, self.segmentsNumber, self.segments))
