from wagtail.blocks import (
    CharBlock,   
    StructBlock,
    URLBlock,
    IntegerBlock,
    BooleanBlock
)

class RSSFeedBlock(StructBlock):
    title = CharBlock(required=True, max_length=255)
    rss_url = URLBlock(required=True)
    max_entries = IntegerBlock(required=False, min_value=1, default=3)
    display_title = BooleanBlock(required=False, default=True)
    display_content = BooleanBlock(required=False, default=True)
    display_author = BooleanBlock(required=False, default=False)
    display_date = BooleanBlock(required=False, default=True)

    class Meta:
        template = "wagtail_rss_feed_block/blocks/rss_feed_block.html"
        icon = "comment"
