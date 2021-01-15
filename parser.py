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


mpd: str = '''<!--  MPD file Generated with GPAC version 0.7.2-DEV-rev289-g1a5a831-master  at 2018-02-26T14:51:24.379Z -->
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.500S" type="static" mediaPresentationDuration="PT0H10M34.650S" maxSegmentDuration="PT0H0M4.000S" profiles="urn:mpeg:dash:profile:full:2011">
<ProgramInformation moreInformationURL="http://gpac.io">
<Title>bbb_enc_x264_dash.mpd generated by GPAC</Title>
</ProgramInformation>
<Period duration="PT0H10M34.650S">
<AdaptationSet segmentAlignment="true" bitstreamSwitching="true" maxWidth="3840" maxHeight="2160" maxFrameRate="60" par="16:9" lang="und">
<SegmentTemplate initialization="bbb_enc_x264_dash_init.mp4"/>
<Representation id="1" mimeType="video/mp4" codecs="avc3.4D4034" width="3840" height="2160" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="39537644">
<SegmentTemplate media="3840x2160/40000kbps/bbb_3840x2160_60fps_40000kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="2" mimeType="video/mp4" codecs="avc3.4D4034" width="3840" height="2160" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="24724258">
<SegmentTemplate media="3840x2160/25000kbps/bbb_3840x2160_60fps_25000kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="3" mimeType="video/mp4" codecs="avc3.4D4034" width="3840" height="2160" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="14817987">
<SegmentTemplate media="3840x2160/15000kbps/bbb_3840x2160_60fps_15000kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="4" mimeType="video/mp4" codecs="avc3.4D402A" width="1920" height="1080" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="4282335">
<SegmentTemplate media="1920x1080/4300kbps/bbb_1920x1080_60fps_4300kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="5" mimeType="video/mp4" codecs="avc3.4D402A" width="1920" height="1080" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="3832741">
<SegmentTemplate media="1920x1080/3850kbps/bbb_1920x1080_60fps_3850kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="6" mimeType="video/mp4" codecs="avc3.4D4020" width="1280" height="720" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="3012836">
<SegmentTemplate media="1280x720/3000kbps/bbb_1280x720_60fps_3000kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="7" mimeType="video/mp4" codecs="avc3.4D4020" width="1280" height="720" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="2358888">
<SegmentTemplate media="1280x720/2350kbps/bbb_1280x720_60fps_2350kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="8" mimeType="video/mp4" codecs="avc3.4D401F" width="736" height="414" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="1815296">
<SegmentTemplate media="736x414/1750kbps/bbb_736x414_60fps_1750kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="9" mimeType="video/mp4" codecs="avc3.4D401F" width="640" height="360" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="1085049">
<SegmentTemplate media="640x360/1050kbps/bbb_640x360_60fps_1050kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="10" mimeType="video/mp4" codecs="avc3.4D401E" width="512" height="288" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="752410">
<SegmentTemplate media="512x288/750kbps/bbb_512x288_60fps_750kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="11" mimeType="video/mp4" codecs="avc3.4D401E" width="512" height="288" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="560890">
<SegmentTemplate media="512x288/560kbps/bbb_512x288_60fps_560kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="12" mimeType="video/mp4" codecs="avc3.4D4016" width="384" height="216" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="380034">
<SegmentTemplate media="384x216/375kbps/bbb_384x216_60fps_375kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
<Representation id="13" mimeType="video/mp4" codecs="avc3.4D4015" width="320" height="180" frameRate="60" sar="1:1" startWithSAP="1" bandwidth="237851">
<SegmentTemplate media="320x180/235kbps/bbb_320x180_60fps_235kbps_segment$Number$.m4s" timescale="60000" startNumber="1" duration="240000"/>
</Representation>
</AdaptationSet>
</Period>
</MPD>'''
bbb = Parser(mpd, 'http://cs1dev.ucc.ie/misl/4K_non_copyright_dataset/4_sec/x264/bbb/DASH_Files/full/bbb_enc_x264_dash.mpd')
bbb.simple()
print(bbb.__dict__)
print(bbb.initialization_url)
print(bbb.get_media_url(3832741, 159))