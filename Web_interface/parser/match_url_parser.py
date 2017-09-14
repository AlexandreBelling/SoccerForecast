from Web_interface.parser.web_html_parser import WebHtmlParser


class MatchUrlParser(WebHtmlParser):

    HOMEPAGE = "https://fr.whoscored.com"

    def __init__(self, season_url):
        super().__init__()
        self.url_list = []
        self.season_url = season_url

    def process_code(self, code_source):
        self.feed(code_source)
        return self.url_list

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attr_dict = {}
            for key, value in attrs:
                attr_dict[key] = value
            try:
                a_class = attr_dict['class']
                if 'match-link' in a_class and 'match-report' in a_class:
                    match_to_append = self.HOMEPAGE + attr_dict['href']
                    match_to_append.replace('MatchReport', 'LiveStatistics')
                    self.url_list.append(match_to_append)
            except KeyError:
                pass