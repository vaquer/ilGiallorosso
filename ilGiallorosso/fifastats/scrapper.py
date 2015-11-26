import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

class FifaScrapper(object):
    def __init__(self, *args, **kwargs):
        self.html_stats = None
        self.html_top_scorers = None
        self.html_matches = None

        self.url_stats = 'http://es.fifa.com/world-match-centre/nationalleagues/nationalleague=italy-serie-a-2000000026/standings/index.html'
        self.url_top_scorers = 'http://es.fifa.com/world-match-centre/nationalleagues/nationalleague=italy-serie-a-2000000026/top-scorers/index.html'
        self.url_matches = 'http://www.fifa.com/world-match-centre/clubs/club=italy-as-roma-31083/matches/index.html'

        self.id_tournament = kwargs.get('id_tournament', '2000000026')

        self.set_stats_html(self.set_html_from_fifa(self.url_stats))
        self.set_json_stats()

        self.set_matches_html(self.set_html_from_fifa(self.url_matches))
        self.set_json_matches()


    def set_html_from_fifa(self, url=None):
        if not url:
            return None

        try:
            html_response = requests.get(url)
            html_response.raise_for_status()
        except requests.exceptions.RequestException, e:
            self.request_error = e
            return None
        else:
            return BeautifulSoup(html_response.text.encode('utf-8'), "html.parser")

    def set_stats_html(self, html_sp=None):
        if not html_sp:
            return None

        for table in html_sp.find_all('table'):
            if table.attrs.get('id', '') == self.id_tournament and 'standings' in table.attrs.get('class', ['']):
                self.html_stats = table

    def set_json_stats(self):
        self.stats = {'italy': []}
        for tr in self.html_stats.tbody.find_all('tr'):
            team = {}
            for td in tr.find_all('td'):
                team.update({'{0}'.format(td.attrs.get('class')[0]): td.get_text()})

                if td.attrs.get('class')[0] == 'diff':
                    team['diff'] = '{0}'.format(td.span)

            team['team'] = team['team'].strip()
            team['champions'] = True if 't-status-64' in tr.attrs.get('class', ['']) else False
            team['champions_preliminary'] = True if 't-status-128' in tr.attrs.get('class', ['']) else False
            team['uefa'] = True if 't-status-1048576' in tr.attrs.get('class', ['']) else False
            team['uefa_dependency'] = True if 't-status-512' in tr.attrs.get('class', ['']) else False
            team['relegation'] = True if 't-status-8' in tr.attrs.get('class', ['']) else False

            self.stats['italy'].append(team)

    def set_matches_html(self, html_soup=None):
        if not html_soup:
            return None

        self.html_matches = html_soup.find("div", {'class': 'm-list'}).div

    def set_json_matches(self):
        self.matches = {'roma': []}
        for div in self.html_matches.find_all('div', {'data-type': 'matches'}):
            match = { 
                'match_id': div.attrs.get('data-id'),
                'date': datetime.fromtimestamp(time.mktime(time.strptime(div.attrs.get('data-matchdate'), '%Y%m%d'))),
                'date_string': div.attrs.get('data-matchdate'),
                'home': div.find('div', {'class': 'home'}).find('span', {'class': 't-nText'}).get_text(),
                'home_logo': div.find('div', {'class': 'home'}).find('img', {'class': 't-i-3-logo'}).attrs.get('src'),
                'away': div.find('div', {'class': 'away'}).find('span', {'class': 't-nText'}).get_text(),
                'away_logo': div.find('div', {'class': 'away'}).find('img', {'class': 't-i-3-logo'}).attrs.get('src'),
            }

            if 'mc-match-is-result' in div.attrs.get('class', ['']):
                match['res'] = div.find('span', {'class': 's-resText'}).get_text()
                match['is_res'] = True
            else:
                match['is_res'] = False

            self.matches['roma'].append(match)

        counter = 0
        for div in self.html_matches.find_all('div', {'class': 'm-head'}):
            competition = 'Serie A TIM' if 'Serie A TIM' in div.find('span', {'class': 'm-compgroup-text'}).get_text() else 'UEFA Champions League'
            self.matches['roma'][counter]['competiton'] = competition


    def get_stats(self):
        return self.stats

    def get_last_match(self):
        matches = {}
        for match in self.matches['roma']:
            if match['is_res']:
                matches['{0}'.format(match['date_string'])] = match

        matches_keys = matches.keys()
        matches_keys.sort()
        return matches['{0}'.format(matches_keys[len(matches_keys) - 1])]

    def get_next_mtach(self):
        matches = {}
        for match in self.matches['roma']:
            if not match['is_res']:
                matches['{0}'.format(match['date_string'])] = match

        matches_keys = matches.keys()
        matches_keys.sort()
        return matches['{0}'.format(matches_keys[0])]

