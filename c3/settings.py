import datetime, pytz
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.default_settings import (
    DEFAULT_ENABLED_NAVBAR_LISTS,
    DEFAULT_ENABLED_PAGES,
    DEFAULT_HOME_ACTIVITY_TABS,
)
from magi.utils import (
    getTranslatedName,
)
from c3.c3_translations import ct
from c3 import models

############################################################
# Basic settings

SITE_NAME = 'C3DeX'
SITE_DESCRIPTION = 'Camp/Congress precious friends and memories personal tracker'
SITE_URL = 'http://c3.db0.company/'
SITE_IMAGE = 'c3.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.c3.db0.company/'
GAME_NAME = 'CCC'
COMMENTS_ENGINE = 'commento'
GOOGLE_ANALYTICS = None
ACCOUNT_MODEL = models.Account
COLOR = '#E3350D'

LAUNCH_DATE = datetime.datetime(2019, 8, 20, 12, 0, 0, tzinfo=pytz.UTC)

############################################################
# About

ABOUT_PHOTO = 'db0.png'

SITE_LONG_DESCRIPTION = """
c3Dex aims to provide a safe place for CCC attendees to keep track of and share their experience,
and make or keep friends.

It's:
- **Anonymous**
    - We don't ask you for any personal details when you sign up.
- **Beginners-friendly**
    - Because we've all been there.
- **Open source**
    - Of course!
"""

GITHUB_REPOSITORY = ('db0company', 'c3DeX')

CONTACT_DISCORD = None
CONTACT_EMAIL = 'db0company@gmail.com'
CONTACT_FACEBOOK = 'db0company'
CONTACT_REDDIT = 'db0company'

GAME_DESCRIPTION = """
The Chaos Communication Congress is an annual four-day conference on technology, society and utopia organised by the Chaos Computer Club (CCC) and volunteers.

The Congress offers lectures and workshops and various events on a multitude of topics including (but not limited to) information technology and generally a critical-creative attitude towards technology and the discussion about the effects of technological advances on society.

The Chaos Communication Camp is an international, five-day open-air event for hackers and associated life-forms. It provides a relaxed atmosphere for free exchange of technical, social, and political ideas. The Camp has everything you need: power, internet, food and fun. Bring your tent and participate!
"""
GAME_URL = 'https://www.ccc.de/en/'

GOOGLE_ANALYTICS = None

############################################################
# Profile

SHOW_TOTAL_ACCOUNTS = False

USER_COLORS = [
    (0, '0xf00', 'red', COLOR),
    (1, '0x0f0', 'green', '#4dad5b'),
    (2, '0x00f', 'blue', '#1b53ba'),
    (3, '0x0ff', 'lightblue', '#30a7d7'),
    (4, '0xf0f', 'pink', '#e05aa8'),
    (5, '0xff0', 'yellow', '#e6bc2f'),
]

############################################################
# Navbar

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS.copy()

ENABLED_NAVBAR_LISTS['links'] = {
    'icon': 'link',
    'titles': _('Links'),
    'url': '/links/',
    'order': [
        u'link-{}'.format(_id)
        for _id in django_settings.LINKS_IN_NAVBAR.keys()
    ] + ['link_list'],
}

ENABLED_PAGES = DEFAULT_ENABLED_PAGES.copy()

for link_id, link in django_settings.LINKS_IN_NAVBAR.items():
    ENABLED_PAGES[u'link-{}'.format(link_id)] = {
        'redirect': link['url'],
        'title': getTranslatedName(link),
        'navbar_link_list': 'links',
    }

############################################################
# Homepage

HOME_ACTIVITY_TABS = DEFAULT_HOME_ACTIVITY_TABS.copy()

# Delete staff picks
del(HOME_ACTIVITY_TABS['staffpicks'])

# Add top tab
HOME_ACTIVITY_TABS['top_all_time'] = {
    'title': string_concat(_('Most Popular'), ' (', _('All time'), ')'),
    'icon': 'trophy',
    'form_fields': {
        'ordering': '_cache_total_likes,creation',
    },
}

CALL_TO_ACTION = ct['Catch\'em all!']

############################################################
# Activities

ACTIVITY_TAGS = [
    ('photo', _('Photo')),
    ('diary', _('Diary')),
    ('project', _('Project')),
    ('question', _('Question')),
    ('comedy', _('Comedy')),
    ('meme', _('MEME')),
    ('questionable', _('Questionable')),
    ('nsfw', _('NSFW')),
]

############################################################
# From settings or generated_settings

STAFF_CONFIGURATIONS = getattr(django_settings, 'STAFF_CONFIGURATIONS', None)
STATIC_FILES_VERSION = django_settings.STATIC_FILES_VERSION
LATEST_NEWS = getattr(django_settings, 'LATEST_NEWS', None)

############################################################
# Staff configurations fallback

if 'about_image' not in STAFF_CONFIGURATIONS:
    STAFF_CONFIGURATIONS['about_image'] = 'about.png'
if 'about_us' not in STAFF_CONFIGURATIONS:
    STAFF_CONFIGURATIONS['about_us'] = {
        'en': """
Nice to meet you, I'm [db0](https://db0.company/).

![I'm old enough to remember when the Internet wasn't a group of five websites, each consisting of screenshots of text from the other four.](https://i.imgur.com/UwhwePE.png)[](https://i.imgur.com/OWi3CM8.png)

### **It's time to give the control back to the communities.**

With this mindset, I started [my own social network
engine](https://github.com/MagiCircles/MagiCircles/wiki/)
a few years ago. It's currently mostly used by gaming communities,
but my goal is to make sure it stays fully open source and easy to use,
to allow communities who need them to create their
own safe spaces and fully keep control over them.

In particular, in the future, I'm hoping it can be of use to communities who I love
and support, but more importantly need safe spaces more than anyone else, such as
communities of transgender people and people with disabilities.

It's still under development, and there are many features I would like to implement. For example,
I'd like to eventually be compatible with [ActivityPub](https://activitypub.rocks/).

I'm a shy person, but I'm passionate about this project, so if you're interested,
please talk to me, at camp/congress or online!
""",
    }
