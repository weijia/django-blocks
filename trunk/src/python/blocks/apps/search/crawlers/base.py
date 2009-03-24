class Crawler(object):
    def __init__(self, backend):
        self.backend = backend
    
    def crawl(self):
        raise NotImplementedError