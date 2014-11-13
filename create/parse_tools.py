"""
tools to help with file parsing for the BUDA social graph
"""

import re
import unicodedata

def format_name(name):
    """
    turn
    Sprong, Kevin
    into
    Kevin Sprong
    also strip out any crazy unicode stuff
    """
    name_match = re.search(r"(.*),\s(.*)", name)
    if name_match:
        name = name_match.group(2) + " " + name_match.group(1)
        normed_name = (unicodedata.normalize('NFKD', name)
                   .encode('ascii', 'ignore')
                   .decode('utf-8'))
        # now get rid of commas
        return re.sub(r",", "", normed_name)
    else:
        print(name)
        quit()


def parse_line(line):
    """
    return player, team, league, season
    from a line of the player_data file
    """
    return line.strip().split('\t')
