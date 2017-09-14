from time import sleep
from .parser.match_url_parser import MatchUrlParser
from selenium.webdriver import Chrome
from pymongo import MongoClient
from dateutil.parser import parse
from datetime import datetime, date
from random import uniform

URL_TOURNAMENT_TEST = "https://fr.whoscored.com/Regions/74/Tournaments/22/France-Ligue-1"
URL_SEASON_TEST = "https://fr.whoscored.com/Regions/74/Tournaments/22/Seasons/5830/France-Ligue-1"
URL_MATCH_TEST = "https://fr.whoscored.com/Matches/960749/MatchReport/France-Ligue-1-2015-2016-Paris-Saint-Germain-Lyon"


class WSUrlRobot(Chrome):

    URL = "https://whoscored.com/LiveScores"
    database = MongoClient().ws_url

    def set(self, proxy_adress, xpath_input, xpath_button):
        super(WSUrlRobot).__init__()
        self.proxy_adress = proxy_adress
        self.xpath_input = xpath_input
        self.xpath_button = xpath_button

    def drop_data(self):
        MongoClient().drop_database('ws_url')

    def get_main_page(self, proxy=True):
        if proxy:
            self.get(self.proxy_adress)
            input = self.find_elements_by_xpath(self.xpath_input)[0]
            input.send_keys(self.URL)
            sleep(uniform(0,3))
            self.find_elements_by_xpath(self.xpath_button)[0].click()
        else:
            self.get(self.URL)

    def get_match_url_on_current(self, verbose=0):
        code_source = self.page_source
        result = MatchUrlParser(self.URL).process_code(code_source)
        if verbose > 0:
            print(result)
        return result

    def get_date(self, verbose):
        date_obj = self.find_elements_by_xpath('//*[@id="date-config-toggle-button"]/span[1]')[0]
        if verbose > 0:
            print(date_obj.text)
        return date_obj.text

    def safe_click_next_day(self):
        date = self.get_date(verbose=0)
        while date == self.get_date(verbose=0):
            try:
                self.click_next_day()
            except:
                pass
            time_to_wait = uniform(0, 1)
            sleep(time_to_wait)

    def reach_date(self, day, month, year):
        # The date button
        self.find_elements_by_xpath('//*[@id="date-config-toggle-button"]')[0].click()
        sleep(1)
        while True:
            try:
                # The year selector button
                self.find_elements_by_xpath("//td[@data-value='%s']" % str(year))[0].click()
                # Pick month
                self.find_elements_by_xpath("//td[@data-value='%s']" % str(month-1))[0].click()
                # Pick day
                self.find_elements_by_xpath("//td[@data-value='%s']" % str(day-1))[-1].click()
                sleep(1)
                break
            except:
                sleep(1)

    def done_retrieving(self):
        date = parse(self.get_date()).timestamp()
        today = parse(date.today().ctime()).timestamp()
        return date > today

    def add_match(self, match_url, date):
            self.database.matches.insert_one({"_id": match_url, "url": match_url, "date": parse(date).timestamp(), "retrieved": False})

    def match_is_new(self, match_url):
            self.database.matches.find_one({"url": match_url}).count() != 0

    def click_next_day(self):
        try:
            element = self.find_elements_by_xpath(
                    '//a[@class="next button ui-state-default rc-l is-default"]'
                )[0]
        except:
            pass
        try:
            element = self.find_elements_by_xpath(
                '//*[@id="date-controller"]/dd[1]/div/a[3]'
                )[0]
        except:
            pass
        element.click()

    def wait_new_day(self):
        element = self.find_elements_by_xpath(
            '//*[@id="livescores"]/table/tbody'
        )
        while len(element) == 0:
            time_to_wait = uniform(0, 1)
            sleep(time_to_wait)
            element = self.find_elements_by_xpath(
                '//*[@id="livescores"]/table/tbody'
            )

    def get_newest_date_in_history(self):
        match_list = self.database.matches.find({})
        date_max = -1
        for match in match_list:
            date_max = max(match["date"], date_max)
        if date_max == -1 or date_max is None:
            result = "1 Aug 2009"
        else :
            result = datetime.fromtimestamp(date_max)
        return result

    def convert_month(self, month):
        mapper = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }
        return mapper[month]

    def parse_history(self, proxy=True, verbose=0):

        date = self.get_newest_date_in_history()
        print(date)
        date = parse(str(date))

        self.get_main_page(proxy)
        self.wait_new_day()
        self.reach_date(date.day, date.month, date.year)

        while not self.done_retrieving():
            try:
                date = self.get_date(verbose)
                list = self.get_match_url_on_current(verbose)
                for match in list:
                    try:
                        self.add_match(match, date)
                    except:
                        print('not added')
                time_to_wait = uniform(0, 1)
                sleep(time_to_wait)
                self.safe_click_next_day()
                self.wait_new_day()

            except:
                self.get_main_page(proxy)
                self.wait_new_day()
                date = self.get_newest_date_in_history()
                date = parse(date)
                self.reach_date(date.day, date.month, date.year)

    def get_perf(self):
        match_to_get = self.database.matches.find({"retrieved": False})
        if match_to_get.count() != 0:
            for match in match_to_get:
                url = match["url"].replace('MatchReport', 'LiveStatistics')
                self.get()


