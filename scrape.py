"""
get roster info from BUDA.org
"""

import requests
import re
from bs4 import BeautifulSoup

def scrape_from_file_links(file_name):
    """
    each line of file_name looks like:

    </tr><tr><td class=infobody colspan=1>
        <a href="/hatleagues/rosters.php?section=showTeamRoster
            &team=2248&which=1093&season=1999">
            Team 5 (5)
        </a> 
    </td>

    we want to access the link and get player names
    """

    # variables to hold info about searched lines
    links = []
    teams = []
    leagues = []
    seasons = []

    num_good_lines = 0
    num_lines = 0
    bad_lines = []

    # get searchable links
    with open(file_name, 'r') as file_in:
        for line in file_in:
            m = re.search(r"/hatleagues/rosters\.php\?section=showTeamRoster&team=(\d+)&which=(\d+)&season=(\d{4})", line)
            if m:
                links.append(m.group(0))
                teams.append(m.group(1))
                leagues.append(m.group(2))
                seasons.append(m.group(3))
                num_good_lines += 1
            else:
                bad_lines.append(line)
            num_lines += 1

    # diagnostic
    """
    print(str(num_good_lines) + " lines out of " +
          str(num_lines) + " had team links") 
    print("bad lines: ")
    for line in bad_lines:
        print(line.strip())
    """

    
if __name__ == "__main__":
    scrape_from_file_links("links.txt")



