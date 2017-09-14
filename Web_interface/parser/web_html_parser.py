from html.parser import HTMLParser


class WebHtmlParser(HTMLParser):

    HOMEPAGE = "https://fr.parser.com"

    def __init__(self):
        self.convert_charrefs = True
        self.reset()
        self.parsedPage = []

    def handle_endtag(self, tag):
        self.parsedPage.append(["end", [tag]])

    def handle_data(self, data):
        self.parsedPage.append(["data", [data]])

    def handle_starttag(self, tag, attrs):
        attr_dict = {}
        for key, value in attrs:
            attr_dict[key] = value
        self.parsedPage.append(["start", [tag, attr_dict]])

    def process_code(self, code_source):
        pass

    def error(self, message):
        pass
