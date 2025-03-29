from src.models.browser import Browser
import browser_cookie3

class FirefoxBrowser(Browser):
    def __init__(self):
        super().__init__("firefox", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")

    def extract_cookies(self):
        return browser_cookie3.firefox(domain_name='meetup.com')

class ChromeBrowser(Browser):
    def __init__(self):
        super().__init__("chrome", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3")

    def extract_cookies(self):
        return browser_cookie3.chrome(domain_name='meetup.com')

class SafariBrowser(Browser):
    def __init__(self):
        super().__init__("safari", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.1")

    def extract_cookies(self):
        return browser_cookie3.safari(domain_name='meetup.com')

class EdgeBrowser(Browser):
    def __init__(self):
        super().__init__("edge", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.")

    def extract_cookies(self):
        return browser_cookie3.edge(domain_name='meetup.com')

class BraveBrowser(Browser):
    def __init__(self):
        super().__init__("brave", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3")

    def extract_cookies(self):
        return browser_cookie3.brave(domain_name='meetup.com')