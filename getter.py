import urllib2
import re

from parser import AnchorExtractor

import errors

contentTypeFilter = re.compile('^text/html(;.*)$')
def isKnownContentType(handle):
    return contentTypeFilter.match(handle.headers.get('content-type', ''))

def getURL(url, timeout, linkFound, target, fetchContent):
    result = None
    try:
        chunks = chunkGenerator(urllib2.urlopen(url, timeout=timeout)) if fetchContent else ()
    except urllib2.HTTPError, error:
        chunks = chunkGenerator(handle=error) if fetchContent else ()
        result = errors.HTTPError(error)
    except urllib2.URLError, error:
        chunks = ()
        result = errors.URLError(error)

    try:
        AnchorExtractor.process(url, chunks, linkFound)
    except errors.HTMLError, error:
        # NOTE: when an HTMLParserError occurs it silently masks previous errors, if any; so there is no way to
        #        differentiate a broken 404 page for a URL and a broken OK page for that URL; I think it is a
        #        non-issue, but refactoring this peculiarity away is not too hard
        result = error

    return result

def chunkGenerator(handle):
    if not isKnownContentType(handle):
        return
    chunk = handle.read(4096)
    while chunk:
        yield chunk
        chunk = handle.read(4096)
