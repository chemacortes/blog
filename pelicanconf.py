#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Chema Cortés"
SITENAME = "Hyperreals *R"
SITESUBTITLE = "Quarks, bits y otras criaturas infinitesimales"
GITHUB_URL = "http://github.com/chemacortes/blog"
SITEURL = ""

PATH = "content"
TIMEZONE = "Europe/Paris"
DEFAULT_LANG = "es"

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

FEED_MAX_ITEMS = 30

# Blogroll
LINKS = (
    ("All Feeds", "/feeds/all.atom.xml"),
    ("Scala Feeds", "/feeds/scala.atom.xml"),
    ("Python Feeds", "/feeds/python.atom.xml"),
    # ('Haskell Feeds','/feeds/haskell.atom.xml'),
    ("my coursera", "https://www.coursera.org/user/9408450118c4cfeddff015451ed358b6"),
)

# Social widget
SOCIAL = (
    ("twitter", "https://twitter.com/chemacortes"),
    ("github", "https://github.com/chemacortes"),
    ("bitbucket", "https://bitbucket.org/chemacortes/"),
    ("stackoverflow", "http://stackoverflow.com/users/1243400/chemacortes"),
    # ('delicious', 'https://delicious.com/chemacortes'),
    # ('google+', 'https://plus.google.com/+ChemaCortés'),
    ("linkedin", "https://linkedin.com/in/chemacortes"),
    # ('facebook', 'https://facebook.com/pych3m4'),
    # ('flickr', 'https://www.flickr.com/photos/chemacortes'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


TYPOGRIFY = True

STATIC_PATHS = ["extra", "pictures", "code"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/README.md": {"path": "README.md"},
    "extra/CNAME": {"path": "CNAME"},
    "extra/google989145ab610d7f0b.html": {"path": "google989145ab610d7f0b.html"},
}
IGNORE_FILES = ["extra"]

INDEX_SAVE_AS = "index.html"
ARCHIVES_URL = "archives.html"
ARCHIVES_SAVE_AS = "archives.html"
ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"
DRAFT_URL = "drafts/{date:%Y}-{date:%m}-{date:%d}-{slug}.html"
DRAFT_SAVE_AS = "drafts/{date:%Y}-{date:%m}-{date:%d}-{slug}.html"
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"

TAGS_URL = "tag/"
TAGS_SAVE_AS = "tag/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

CATEGORIES_URL = "category/"
CATEGORIES_SAVE_AS = "category/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

AUTHORS_URL = ""  # 'blog/authors/'
AUTHORS_SAVE_AS = ""  # 'blog/authors/index.html'
AUTHOR_URL = ""  # 'blog/authors/{slug}.html'
AUTHOR_SAVE_AS = ""  # 'blog/authors/{slug}.html'


THEME = "pelican-subtle-mod"

PLUGIN_PATHS = [
    "plugins",
    "pelican-subtle-mod/plugins",
    "pelican-plugins",
]
PLUGINS = [
    #    "assets",
    "pelican_webassets",
    "render_math",
    "sitemap",
    "neighbors",
    "liquid_tags",
    "liquid_tags.img",
    "liquid_tags.audio",
    "liquid_tags.video",
    "liquid_tags.youtube",
    "liquid_tags.vimeo",
    "liquid_tags.include_code",
    "plantuml",
]
# DIRECT_TEMPLATES = ('index', 'tags', 'categories','archives')

MARKDOWN = {
    "extension_configs": {
        "mdx_include": {},
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "guess_lang": False,
            "linenums": False,
        },
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.admonition": {},
    },
    "output_format": "html5",
}


SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.9, "indexes": 0.5, "pages": 0.3},
    "changefreqs": {"articles": "monthly", "indexes": "weekly", "pages": "yearly"},
}

MATH_JAX = {
    "equation_numbering": "AMS",
}

# Theme specific
DISPLAY_META_ABOVE_ARTICLE = True
FUZZY_DATES = True
TAGLINE = "Quarks, bits y otras criaturas infinitesimales"
USER_LOGO_URL = "https://s.gravatar.com/avatar/b20d114964d6d77c209aadbe9a152e87?s=80"
# DISQUS_SITENAME = "hyperreals"
# DISQUS_COLLAPSED = True
GLOBAL_KEYWORDS = [
    "functional programming",
    "programming",
    "programación",
    "lambda calculus",
    "math",
]
