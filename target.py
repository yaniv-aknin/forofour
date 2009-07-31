class StandardOutputTarget:
    def __init__(self):
        self.alreadyReported = set()
    def report(self, referer, url, error):
        if (referer, url, error) in self.alreadyReported:
            return
        print '{0[result]:5} {0[url]} (<- {0[referer]}) {0[error]}'.format(dict(
                result = 'OK' if error is None else 'ERROR',
                url = url,
                referer = referer,
                error = '' if error is None else error,
            ))
        self.alreadyReported.add((referer, url, error))
