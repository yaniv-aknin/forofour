from functools import partial
import re
from urlparse import urljoin, urlparse, urlunparse

from twisted.application.service import Service
from twisted.internet import defer
from twisted.internet.threads import deferToThread

from getter import getURL

class Crawler(Service):
    supportedSchemes = ('http', 'https')
    def __init__(self, options, target, start):
        self.options = options
        self.runningGetters = 0
        self.target = target
        self.start = start
        self.startNetloc = urlparse(start).netloc
        self.resultCache = {}
        self.tasks = []
        self.lifetime = defer.Deferred()
    def startService(self):
        Service.startService(self)
        self.startGetter('START', self.start)
    def stopService(self):
        Service.stopService(self)
        return self.lifetime
    def startGetter(self, referer, url):
        if url in self.resultCache:
            return self.processResult(referer, url, self.resultCache[url], updateCache=False)
        self.runningGetters += 1
        # NOTE: if the URL we are retrieving is on a different net location, we will not bother fetching its contents,
        #        just the HTTP header for the response code; not fetching its contents also means not parsing its links
        #        which means we will never descend into the link hierarchy of a foreign netloc
        d = deferToThread(getURL, url, self.options.fetchTimeout, partial(self.linkFound, url), self.target,
                          fetchContent=(urlparse(url).netloc == self.startNetloc))
        d.addCallback(lambda error: self.processResult(referer, url, error))
        d.addErrback(lambda failure: self.unhandledGetterException(failure, url))
        d.addBoth(self.cleanupGetter)
    def linkFound(self, referer, base, href):
        destination = urlparse(urljoin(base, href))
        if destination.scheme not in self.supportedSchemes:
            return
        # NOTE: we intentionally pass '' as the fragment, since we do not care about fragments
        destination = urlunparse((destination.scheme, destination.netloc, destination.path,
                                  destination.params, destination.query, ''))
        self.tasks.append((referer, destination))
    def processResult(self, referer, url, error, updateCache=True):
        if updateCache:
            self.resultCache[url] = error
        self.target.report(referer, url, error)
    def unhandledGetterException(self, failure, url):
        print 'UNHANDLED EXCEPTION handling url %s:' % (url,)
        failure.printTraceback()
    def cleanupGetter(self, dummyValue):
        self.runningGetters -= 1
        while self.running and self.tasks and self.runningGetters < self.options.concurrent:
            referer, url = self.tasks.pop(0)
            self.startGetter(referer, url)
        if not self.running and not self.runningGetters:
            self.lifetime.callback(None)
