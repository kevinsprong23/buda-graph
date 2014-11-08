"""
get roster info from BUDA.org
"""

import requests
import re
from bs4 import BeautifulSoup
from time import sleep

def parse_file_links(file_name):
    """
    each line of file_name looks like:

    </tr><tr><td class=infobody colspan=1>
        <a href="/hatleagues/rosters.php?section=showTeamRoster
            &team=2248&which=1093&season=1999">
            Team 5 (5)
        </a> 
    </td>
    
    this method returns a dictionary of 
    4 lists, all of same length: 
    1) the links themselves
    2) the team ids
    3) the league ids
    4) the seasons
    
    """

    # variables to hold info about searched lines
    d = {}
    d['links'] = []
    d['teams'] = []
    d['leagues'] = []
    d['seasons'] = []

    # get searchable links
    with open(file_name, 'r') as file_in:
        for line in file_in:
            m = re.search(r"/hatleagues/rosters\.php\?section=showTeamRoster&team=(\d+)&which=(\d+)&season=(\d{4})", line)
            if m:
                d['links'].append(m.group(0))
                d['teams'].append(m.group(1))
                d['leagues'].append(m.group(2))
                d['seasons'].append(m.group(3))
    
    return d

def scrape_buda(link_info, file_name_out):
    """
    link_info is the dict of links, teams, leagues, seasons
    """

    # get the player names, and put them in a .tsv file with team/league info
    with open(file_name_out, 'w') as file_out:
        base_url = "http://buda.org"
        for i, link in enumerate(d['links']):
            # pause between requests, because I am a gentleman
            sleep(3)

            # get and parse the team info
            r = requests.get(base_url + link)
            soup = BeautifulSoup(r)
            for player in soup.findAll('td', 'infobody'):
                file_out.write('\t'.join((player,
                                         d['teams'][i],
                                         d['leagues'][i],
                                         d['seasons'][i])) 
                               + '\n')
 

if __name__ == "__main__":
    """ use existing file """
    d = parse_file_links("data/links.txt")
    scrape_buda(d, "data/player_data.tsv")


