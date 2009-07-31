#!/usr/bin/env python2.6

import sys
import logging

from twisted.internet import reactor, defer
from twisted.application import internet

from argument_parsing import parseArguments
from crawler import Crawler
from target import StandardOutputTarget
from manhole import ManholeTelnetFactory

def main(argv):
    options, startURLs = parseArguments(argv[1:])
    reactor.suggestThreadPoolSize(options.concurrent)

    crawlers = dict((startURL, Crawler(options, StandardOutputTarget(), startURL)) for startURL in startURLs)
    for crawler in crawlers.values():
        crawler.startService()

    lifetime = defer.DeferredList([crawler.lifetime for crawler in crawlers.values()])
    lifetime.addBoth(lambda dummy: reactor.stop())

    manhole = internet.TCPServer(2323, ManholeTelnetFactory(locals()), interface='127.0.0.1')
    manhole.startService()

    reactor.run()

if __name__ == '__main__':
    main(sys.argv)
