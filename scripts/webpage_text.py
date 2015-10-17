from scripts import Scripts
import requests
from BeautifulSoup import BeautifulSoup

class WebPageText(Scripts):
    host = []
    strings_to_match = []

    def __init__(self, host, strings_to_match = [], **kwargs):
        self.host = host
        self.strings_to_match = strings_to_match

        #pass remaining arguments to the parent class
        super(WebPageText, self).__init__(**kwargs)

    def __str__(self):
        return "<%s:%s>" % (self.host, ", ".join(self.strings_to_match))

    def do_test(self):
        r = requests.get(self.host)
        if r.status_code != 200:
            self.failed("%s did not load with HTTP OK, but with: %s" % (self, r.status_code))
            return

        soup = BeautifulSoup(r.text)
        html_textnodes = soup.findAll(text=True)
        html_textnodes = unicode.join(u'\n',map(unicode, html_textnodes))

        for txt in self.strings_to_match:
            if txt in html_textnodes:
                self.passed("%s found in %s" % (txt, self.host))
            else:
                self.failed("%s NOT found in %s" % (txt, self.host))
