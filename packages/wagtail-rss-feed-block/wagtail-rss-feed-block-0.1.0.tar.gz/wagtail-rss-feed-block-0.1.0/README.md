
# Wagtail RSS feed

Wagtail RSS feed is a Django app that provides custom content block that can be used with any Wagtail page model.

This way you can load any RSS feed and display it on a any Wagtail page.

## Quick start

1. Install "wagtail_rss_feed_block" using pip
    
    ```
    $ pip install wagtail-rss-feed-block
    ```

2. Add "wagtail_rss_feed_block" to your INSTALLED_APPS setting like this:

    ```
    INSTALLED_APPS = [
        ...,
        "wagtail_rss_feed_block",
    ]
    ```

3. Use RSSFeedBlock in your Wagtail Page model for example like this:

    ```
    from wagtail.models import Page
    from wagtail.fields import StreamField
    from wagtail_rss_feed_block.blocks import RSSFeedBlock

    class BlogPage(Page):
        body = StreamField([
            ...
            ('rss_feed', RSSFeedBlock()),
            ...
        ])

        content_panels = [       
            FieldPanel('body'),
        ]
    ```

4. Make and apply database migrations with new changes:

    ```
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

## Development

1. Clone this repo:
    
    ```
    $ git clone git@github.com:LESPROJEKT/wagtail-rss-feed-block.git
    ```

2. Use pip to install this package from newly cloned repo folder to your local Django project ( -e argument stands for --editable and it's handy for local development. It will reload your Django project every time you make changes to wagtail-rss-feed-block.):
    
    ```
    $ pip install -e <path to repo folder>
    ```

3. Now you can continue from step no. 2 of Quick start guide above.

