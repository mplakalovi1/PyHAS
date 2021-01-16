import logging


class Algorithm:
    def __init__(self, bitrates: list):
        self.__bitrates = bitrates  # available bit rates for segments
        self.__buffer: float = 0
        self.__previous = list()  # list of all previous bit rates determined by algorithm
        self.__usersbandwidth = list()  # list of user's bandwidth

    @property
    def bitrates(self):
        return self.__bitrates

    @property
    def buffer(self):
        return self.__buffer

    @buffer.setter
    def buffer(self, value: float):
        self.__buffer = value
        if self.__buffer < 0:
            logging.info("BUFFER STALLED {} seconds".format(abs(self.__buffer)))
            self.__buffer = 0
        else:
            logging.info("Buffer = {} seconds".format(self.__buffer))

    @property
    def previous(self):
        return self.__previous

    @previous.setter
    def previous(self, value: int):
        self.__previous.append(value)

    @property
    def usersbandwidth(self):
        return self.__usersbandwidth

    @usersbandwidth.setter
    def usersbandwidth(self, value: float):
        self.__usersbandwidth.append(value)


class Algorithm1(Algorithm):  # multiple hops if it's possible
    def alg(self):
        for i in range(len(self.bitrates)):  # finding best possible bit rate considering user's bandwidth
            if self.bitrates[-i - 1] <= self.usersbandwidth[-1]:
                self.previous = self.bitrates[-i - 1]
                return
        self.previous = self.bitrates[0]  # if user's bw is under all bit rates choose the smallest quality


class Algorithm2(Algorithm):  # for smoother transitions (one hop up or down)
    def alg(self):
        index = self.bitrates.index(self.previous[-1])  # index of previous segment's bit rate

        if self.usersbandwidth[-1] < self.previous[-1]:
            if index == 0:
                self.previous = self.bitrates[index]  # choose smallest if previous was also smallest
                return
            else:
                self.previous = self.bitrates[index - 1]
                return
        elif self.usersbandwidth[-1] == self.previous[-1]:
            self.previous = self.bitrates[index]
            return
        else:
            if index == len(self.bitrates) - 1:
                self.previous = self.bitrates[index]
                return
            else:
                self.previous = self.bitrates[index + 1]
