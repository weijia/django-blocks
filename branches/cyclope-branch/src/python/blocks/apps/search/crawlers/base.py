class Crawler(object):
    def __init__(self, backend, verbosity):
        self.backend = backend
        self.backend.verbosity = verbosity
    
    def crawl(self):
        raise NotImplementedError