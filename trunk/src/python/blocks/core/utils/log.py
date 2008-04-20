import os.path
import logging

_ROOT = None

DEBUG = logging.DEBUG
INFO  = logging.INFO

def initialize(level = logging.DEBUG, outfile = None, format = "%(asctime)s %(levelname)s %(name)s: %(message)s"):
    global _ROOT
    
    if _ROOT is None:
        if isinstance(level, dict):
            levels = level
            level = levels.pop('root', logging.DEBUG)
        else:
            levels = {}
                
        _ROOT = logging.root
        _ROOT.setLevel(level)
        formatter = logging.Formatter(format)
        
        streamout = logging.StreamHandler()
        streamout.setLevel(level)
        streamout.setFormatter(formatter)
        _ROOT.addHandler(streamout)
            
        if outfile:
            parts = outfile.split(":")
            if len(parts) == 3:
                fname, sz, ct = parts
                fileout = logging.handlers.RotatingFileHandler(fname, maxBytes=sz, backupCount=ct)
            else:
                fileout = logging.FileHandler(outfile)
                
            fileout.setLevel(level)
            fileout.setFormatter(formatter)
            _ROOT.addHandler(fileout)
        
        for key in levels:
            l = getLogger(key)
            l.setLevel(levels[key])
        
        log = logging.getLogger("blocks")
        log.debug("loaded config")
