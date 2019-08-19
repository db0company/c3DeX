from collections import OrderedDict

MEDIA_API_URL = 'https://api.media.ccc.de/public/'

SCHEDULES = {
    2016: 'https://github.com/nexus511/33c3-fahrplan/raw/master/Fahrplan/schedule.json',
    2017: 'https://fahrplan.events.ccc.de/congress/2017/Fahrplan/schedule.json',
    2018: 'https://fahrplan.events.ccc.de/congress/2018/Fahrplan/schedule.json',
}

CCCS = OrderedDict([
    (1984, 'CCC\'84 nach Orion\'64'),
    (1985, 'Du Darfst'),
    (1986, 'Damit Sie auch morgen noch...'),
    (1987, 'Offene Netze, \'Jetzt!'),
    (1988, 'Ich glaub\' es hackt'),
    (1989, 'Offene Grenzen: Cocomed zuhauf'),
    (1990, '-ohne Motto-'),
    (1991, 'Per Anhalter durch die Netze'),
    (1992, 'Es liegt was in der Luft'),
    (1993, 'Ten years after Orwell'),
    (1994, 'Internet im Kinderzimmer...'),
    (1995, 'Pretty good piracy...'),
    (1996, 'Der futurologische Congress...'),
    (1997, 'Nichts ist wahr. Alles ist erlaubt.'),
    (1998, 'All Rights Reversed'),
    (1999, '16C3'),
    (2000, 'Explicit Lyrics'),
    (2001, 'Hacking is not a crime'),
    (2002, 'Out of Order'),
    (2003, 'Not a Number'),
    (2004, 'The Usual Suspects'),
    (2005, 'Private Investigations'),
    (2006, 'Who can you trust?'),
    (2007, 'Volldampf voraus!'),
    (2008, 'Nothing to hide'),
    (2009, 'Here be dragons'),
    (2010, 'We come in peace'),
    (2011, 'Behind enemy lines'),
    (2012, 'Not my department'),
    (2013, '30C3'),
    (2014, 'A New Dawn'),
    (2015, 'Gated Communities'),
    (2016, 'Works For Me'),
    (2017, 'tuwat'),
    (2018, 'Refreshing Memories'),
])
