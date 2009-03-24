try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
#import pyparsing

START, END, TERM = ("start", "end", "term")
RELEVANCE = 0
