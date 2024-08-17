class LeapSecondsDataUnavailable(Exception):
    def __init__(self, urls):

        message = "'tai-utc.dat' could not be downloaded. URLS tried: {}".format(urls)
        super(self.__class__, self).__init__(message)
