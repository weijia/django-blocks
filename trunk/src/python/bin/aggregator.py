#!/usr/bin/env python
"""
Requires Mark Pilgrim's excellent
Universal Feed Parser (http://feedparser.org)
"""

import os
import time
import optparse
import datetime
import feedparser
import re

def update_feeds(verbose=False):
    from blocks.apps.aggregator.models import Feed, FeedItem
    for feed in Feed.objects.all():
        if verbose:
            print feed
        
        #feedparser._HTMLSanitizer.acceptable_attributes = ['align', 'alt', 'cols', 'colspan', 'height', 'href', 'rows', 'rowspan', 'span', 'src', 'valign', 'width']
        
        parsed_feed = feedparser.parse(feed.feed_url)
        for entry in parsed_feed.entries:
            title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")
            link = entry.link.encode(parsed_feed.encoding, "xmlcharrefreplace")

            if not guid:
                guid = link
                
            if hasattr(entry, "summary"):
                summary = entry.summary
            elif hasattr(entry, "description"):
                summary = entry.description
            else:
                summary = u""
            summary = summary.encode(parsed_feed.encoding, "xmlcharrefreplace")

            if hasattr(entry, "content"):
                content = entry.content[0].value
            else:
                content = summary
            content = content.encode(parsed_feed.encoding, "xmlcharrefreplace")
            
            # fix content
            from blocks.core.utils import strip_tags
            content = strip_tags(content)
            content = re.sub(r'<!--[\s\S\n]*-->', '', content)
            content = re.sub(r'<p>[\s\n]</p>', '', content)
            content = re.sub(r'<p[\s]*/>', '', content)
            content = content.strip()

            try:
                if entry.has_key('modified_parsed'):
                    date_modified = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
                elif parsed_feed.feed.has_key('modified_parsed'):
                    date_modified = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.feed.modified_parsed))
                elif parsed_feed.has_key('modified'):
                    date_modified = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.modified))
                else:
                    print "no date field found"
                    date_modified = datetime.datetime.now()
            except TypeError:
                date_modified = datetime.datetime.now()

            try:
                feed.feeditem_set.get(guid=guid)
            except FeedItem.DoesNotExist:
                feed.feeditem_set.create(title=title, link=link, summary_html=summary, content_html=content, guid=guid, date_modified=date_modified)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    parser.add_option('-v', '--verbose', action="store_true")
    options, args = parser.parse_args()
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    update_feeds(options.verbose)
