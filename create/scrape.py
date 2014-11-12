"""
get roster info from BUDA.org
"""

import requests
import re
from bs4 import BeautifulSoup
from time import sleep

def parse_file_links(file_name):
    """
    each line of file_name looks like (without the newlines):

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
    data = {}
    data['links'] = []
    data['teams'] = []
    data['leagues'] = []
    data['seasons'] = []

    # get searchable links
    with open(file_name, 'r') as file_in:
        for line in file_in:
            m = re.search(r"/hatleagues/rosters\.php\?section=showTeamRoster&team=(\d+)&which=(\d+)&season=(\d+)", line)
            if m:
                data['links'].append(m.group(0))
                data['teams'].append(m.group(1))
                data['leagues'].append(m.group(2))
                data['seasons'].append(m.group(3))

    return data


def scrape_buda(data, file_name_out):
    """
    data is the dict of links, teams, leagues, seasons
    TODO HANDLE THE TEAMS THAT MIGHT DIVIDE ROSTERS OVER TWO PAGES
    """

    # get the player names, and put them in a .tsv file with team/league info
    with open(file_name_out, 'w') as file_out:
        base_url = "http://buda.org"
        for i, link in enumerate(data['links']):
            # pause between requests, because I am a gentleman
            sleep(4)

            # get and parse the team info
            print(link, flush=True)
            r = requests.get(base_url + link)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text)
            for item in soup.findAll('td', 'infobody'):
                player = item.get_text().strip()
                if player:
                    print(player, data['teams'][i], data['leagues'][i],
                          data['seasons'][i], sep='\t', file=file_out)


if __name__ == "__main__":
    # use links file
    data = parse_file_links("data/links.txt")
    scrape_buda(data, "data/roster_data.tsv")



