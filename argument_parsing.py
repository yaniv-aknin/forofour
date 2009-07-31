import optparse

def parseArguments(argv):
    parser = optparse.OptionParser()
    parser.add_option("-c", "--concurrent", help="how many simultaneous crawl requests to send", type=int)
    parser.add_option("-t", "--fetch-timeout", dest='fetchTimeout', help="timeout per page fetch", type=int)
    parser.set_defaults(concurrent=1, fetchTimeout=60)
    options, arguments = parser.parse_args()
    if not arguments:
        parser.error('expected at least one URL as an argument')
    return options, arguments
