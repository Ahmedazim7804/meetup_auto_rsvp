from models.query import BaseQuery
from loguru import logger
from models.cookies import BaseCookies
from models.headers import BaseHeaders
from client.browsers import FirefoxBrowser, ChromeBrowser, SafariBrowser, EdgeBrowser, BraveBrowser
from models.browser import Browser
from typing import Any, NamedTuple
import requests

class BaseCookiesResult(NamedTuple):
    cookies: BaseCookies
    browser: Browser

class Client:
    def __init__(self):
        self.session = requests.session()

        cookiesRes : BaseCookiesResult = self.getBaseCookies()
        cookies: BaseCookies = cookiesRes.cookies
        headers: BaseHeaders = self.getHeaders(cookiesRes.browser)

        for cookie in cookies:
            self.session.cookies[cookie] = cookies[cookie]

        for header in headers:
            self.session.cookies[header] = headers[header]

    
    def getBaseCookies(self) -> BaseCookiesResult:
        browsers : list[Browser] = [
            FirefoxBrowser(),
            ChromeBrowser(),
            SafariBrowser(),
            EdgeBrowser(),
            BraveBrowser(),
        ]

        cookiejar = None
        selected_browser = None

        for browser in browsers:
            try:
                cookiejar = browser.extract_cookies()
                if cookiejar != None:
                    selected_browser = browser
                    break
            except Exception as e:
                logger.warning(f"Get cookie from {browser.__name__} failed: {e}")
    
        if cookiejar == None or selected_browser == None:
            raise Exception("No cookies found")
    
        cookies: BaseCookies = BaseCookies()

        for cookie in cookiejar:
            cookies[cookie.name] = cookie.value

        return BaseCookiesResult(cookies, selected_browser)

    def getHeaders(self, browser: Browser) -> BaseHeaders:

        if browser == None:
            raise Exception("Browser is required for proper user-agent")

        headers: BaseHeaders = BaseHeaders(
            Accept="*/*",
            Origin="https://www.meetup.com",
            Referer="https://www.meetup.com/",
            Connection="keep-alive",
            Priority="u=4",
        )

        headers["User-Agent"] = browser.user_agent
        headers["Accept-Language"] = 'en-US'
        headers['content-type'] = "application/json"
        headers['apollographql-client-name'] = "nextjs-web"
        headers['x-meetup-view-id'] = ""
        headers['sentry-trace'] = ""
        headers['Sec-Fetch-Dest'] = "empty"
        headers['Sec-Fetch-Mode'] = "cors"
        headers['Sec-Fetch-Site'] = "same-origin"

        return headers


    def executeQuery(self, query: BaseQuery) -> Any | None:

        try:
            logger.debug(f"Executing query: {query.queryName} for {query.queryDesc}")

            response = self.session.post(url=query.url, json=query.params,)

            if response.status_code != 200:
                raise Exception(f"Failed to execute query: {query.queryName} for {query.queryDesc}")

            return query.scrape(response.json())

        except Exception as e:
            logger.error(f"Failed to execute query: {query.queryName} for {query.queryDesc}: {e}")
            return None
       
        