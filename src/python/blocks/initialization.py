import logging
import settings
from core.utils import log

file_path = None
try:
    template_path = settings.BLOCKS_LOGGING_FILE
except AttributeError:
    pass

if file_path is None:
    log.initialize()
else:
    log.initialize(outfile=BLOCKS_LOGGING_FILE)