from email import header
from models.query import BaseQuery
import browser_cookie3
from loguru import logger
from models.cookies import BaseCookies
from models.headers import BaseHeaders
from client.browsers import FirefoxBrowser, ChromeBrowser, SafariBrowser, EdgeBrowser, BraveBrowser
from models.browser import Browser
from typing import _TypedDict, Any, NamedTuple, TypedDict, cast
import requests
import json

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
            # browser_cookie3.firefox,
            # browser_cookie3.chrome,
            # browser_cookie3.safari,
            # browser_cookie3.edge,
            # browser_cookie3.brave,
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


    def executeQuery(self, query: BaseQuery) -> Any:

        logger.debug(f"Executing query: {query.queryName} for {query.queryDesc}")

        # with open('file.json') as f:
        #     response = json.load(f)


        response = self.session.post(url=query.url, json=query.params,)

        if response.status_code != 200:
            raise Exception(f"Failed to execute query: {query.queryName} for {query.queryDesc}")

        return query.scrape(response.json())

        # response = {"data":{"self":{"id":"468792084","isOrganizer":False,"memberships":{"pageInfo":{"hasNextPage":False,"endCursor":"MTc0MTY4NzgxNDAwMA==","__typename":"PageInfo"},"edges":[{"node":{"id":"34441441","name":"Traveling Souls - Cost Share Basis","link":"https://www.meetup.com/travelingsoulsdotorg","city":"Delhi","urlname":"travelingsoulsdotorg","state":"","country":"in","timezone":"Asia/Kolkata","groupPhoto":{"id":"526225796","baseUrl":"https://secure-content.meetupstatic.com/images/classic-events/","__typename":"PhotoInfo"},"organizer":{"id":"33158222","__typename":"Member"},"stepUpInfo":{"organizerNominees":[],"closingDate":None,"__typename":"StepUpInfo"},"__typename":"Group","isPrimaryOrganizer":False,"status":"PAID"},"__typename":"MemberGroupEdge"},{"node":{"id":"37892639","name":"The Coding Bus","link":"https://www.meetup.com/the-coding-bus","city":"Delhi","urlname":"the-coding-bus","state":"","country":"in","timezone":"Asia/Kolkata","groupPhoto":{"id":"526110744","baseUrl":"https://secure-content.meetupstatic.com/images/classic-events/","__typename":"PhotoInfo"},"organizer":{"id":"464852107","__typename":"Member"},"stepUpInfo":{"organizerNominees":[],"closingDate":None,"__typename":"StepUpInfo"},"__typename":"Group","isPrimaryOrganizer":False,"status":"PAID"},"__typename":"MemberGroupEdge"},{"node":{"id":"17357882","name":"Central Delhi Toastmasters Club","link":"https://www.meetup.com/central-delhi-toastmasters-club-cdtm","city":"Delhi","urlname":"central-delhi-toastmasters-club-cdtm","state":"","country":"in","timezone":"Asia/Kolkata","groupPhoto":{"id":"524000009","baseUrl":"https://secure-content.meetupstatic.com/images/classic-events/","__typename":"PhotoInfo"},"organizer":{"id":"174859872","__typename":"Member"},"stepUpInfo":{"organizerNominees":[{"id":"176134082","__typename":"Member"}],"closingDate":None,"__typename":"StepUpInfo"},"__typename":"Group","isPrimaryOrganizer":False,"status":"PAID"},"__typename":"MemberGroupEdge"}],"__typename":"MemberGroupConnection"},"__typename":"Member"}}}
        # query.scrape(response)
       
        