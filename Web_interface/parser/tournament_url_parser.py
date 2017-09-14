from Web_interface.parser.web_html_parser import WebHtmlParser


class TournamentUrlParser(WebHtmlParser):

    HOMEPAGE = "https://fr.parser.com"

    def __init__(self):
        super().__init__()
        self.payload = []
        self.parsedArray = []
        self.target = ''
        self.url_list = []

    def extract_target_script(self):
        for tag in self.parsedPage:
            if tag[0] == "data":
                firstchar = tag[1][0][:20]
                if 'var allRegions' in firstchar:
                    self.target = tag[1][0]
                    return

    def extract_js_array(self):
        self.target = self.target.replace('\n', '')
        self.parsedArray = self.target.split(';')[0]
        self.parsedArray = self.parsedArray.split(' = ')[1]

    def parse_url(self):
        split = self.parsedArray.split('url:')
        split.pop(0)
        for segment in split:
            self.clean_and_add(segment)
        self.url_list

    def clean_and_add(self, segment):
        segment = segment.split(',')[0]
        segment = segment.replace('\'', '')
        self.url_list.append(self.HOMEPAGE+segment)
        return self.url_list

    def process_code(self, code_source):
        self.feed(code_source)
        self.extract_target_script()
        self.extract_js_array()
        self.parse_url()
        return self.url_list
