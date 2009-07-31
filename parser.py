from HTMLParser import HTMLParser, HTMLParseError

import errors

class AnchorExtractor(HTMLParser):
    def __init__(self, base, hrefCallback):
        HTMLParser.__init__(self)
        self.base = base
        self.hrefCallback = hrefCallback
    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return
        # FIXME: the pathological case <a href='x' href='y'> would silently choose 'x' here
        for key, value in dict(attrs).items():
            if key.lower() == 'href':
                self.hrefCallback(self.base, value)
    @classmethod
    def process(cls, url, chunks, linkFound):
        try:
            extractor = cls(base=url, hrefCallback=linkFound)
            for chunk in chunks:
                extractor.feed(chunk)
            extractor.close()
        except HTMLParseError, error:
            raise errors.HTMLError(error)
