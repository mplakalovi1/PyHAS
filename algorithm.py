class Algorithm:
    def __init__(self, bandwidths: list):
        self.bandwidths = bandwidths  # available bandwidths for segments

    def algorithm_1(self, usersbandwidth):  # multiple hops if it's possible
        self.bandwidths.sort(reverse=True)  # bandwidths sorted in descending order

        for segment in self.bandwidths:  # finding best possible segment's quality considering user's bandwidth
            if segment <= usersbandwidth:
                return segment

        return self.bandwidths[len(self.bandwidths) - 1]  # if user's bw is under all segments bw's choose the smallest quality

    def algorithm_2(self, userbandwidth, previous):  # for smoother transitions (one hop up or down)
        index = self.bandwidths.index(previous)  # index of previous segment's bw

        if userbandwidth < previous:
            if index == 0:
                return self.bandwidths[0]  # choose smallest if previous was also smallest
            else:
                return self.bandwidths[index - 1]
        elif userbandwidth == previous:
            return self.bandwidths[index]
        else:
            if index == len(self.bandwidths) - 1:
                return self.bandwidths[len(self.bandwidths) - 1]
            else:
                return self.bandwidths[index + 1]
