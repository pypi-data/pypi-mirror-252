from django import template
import feedparser
import bleach
import time
from datetime import datetime

register = template.Library()

BLEACH_ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
    'li', 'ol', 'strong', 'ul', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'br', 'hr', 'div', 'span', 'img',
]

@register.filter
def get_feed_data(rss_url):
    feed = feedparser.parse(rss_url)
    return feed

@register.filter
def bleach_sanitize(value):
    cleaned_value = bleach.clean(value, tags=BLEACH_ALLOWED_TAGS, attributes=bleach.ALLOWED_ATTRIBUTES)
    return cleaned_value

@register.filter
def get_feed_datetime(entry):
    if hasattr(entry, "published_parsed"):
        return datetime.fromtimestamp(time.mktime(entry.published_parsed))
    elif hasattr(entry, "updated_parsed"):
        return datetime.fromtimestamp(time.mktime(entry.updated_parsed))
    else:
        return None
