from Web_interface.parser.web_html_parser import WebHtmlParser


class SeasonUrlParser(WebHtmlParser):

    HOMEPAGE = "https://fr.parser.com"

    def __init__(self):
        super().__init__()
        self.url_list = []

    def handle_starttag(self, tag, attrs):
        if tag == 'option':
            for key, value in attrs:
                if 'Seasons' in value:
                    self.url_list.append(self.HOMEPAGE+value)

    def process_code(self, code_source):
        self.feed(code_source)
        return self.url_list
