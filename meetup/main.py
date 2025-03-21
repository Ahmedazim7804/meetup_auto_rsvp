# import requests
# from models.group import Group
from models.query import BaseQuery
from client.meetup_client import Client
from enums import QueryMethod

# cookies = {
#     'MEETUP_BROWSER_ID': 'id=03593dbe-960c-4b7b-9ea2-ab580e92a4cc',
#     'MEETUP_TRACK': 'id=2c23958b-d6c3-4fe1-ac48-1bd0effa2092',
#     'LOGGED_OUT_HOMEPAGE_SEGMENTATION': 'spotlight_hero_social_proof',
#     '__stripe_mid': 'daa18f66-e96d-4d0e-a32b-52474e1c5ecb2317b6',
#     'memberId': '468792084',
#     'isSpooner': 'false',
#     'MEETUP_SESSION': 'bc184049-375c-42a8-b7a3-5e9d63dfaca1',
#     '__meetup_auth_access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0Njg3OTIwODQiLCJuYmYiOjE3NDE2ODczMDAsInJvbGUiOiJmaXJzdF9wYXJ0eSIsImlzcyI6Ii5tZWV0dXAuY29tIiwicXVhbnR1bV9sZWFwZWQiOmZhbHNlLCJyZWZyZXNoX3Rva2Vuc19jaGFpbl9pZCI6IjczYTU0NzgyLTRiYjAtNDE1OS04NjBlLWIxZDc3YWI0ZTBlMCIsImV4cCI6MTc0MTY5MDkwMCwiaWF0IjoxNzQxNjg3MzAwLCJqdGkiOiI0ZjZlM2IwYS1lNGUzLTQzOTMtOTAwYi03MmM3NjMzYWUyYjUifQ.htNbt38JrUIh1EsMoAYeVK1yNTLOWiYnAwu1_He0XXk4R2YWcksj4zvdJG8CJ9sVcm_sS4MzoVWIwn1xNVXaSA',
#     'ab.storage.deviceId.4e505175-14eb-44b5-b07f-b0edb6050714': '%7B%22g%22%3A%22f3bea9e6-d37b-0a33-d612-ac4f9bfb65dc%22%2C%22c%22%3A1741687301663%2C%22l%22%3A1741787396469%7D',
#     'ab.storage.userId.4e505175-14eb-44b5-b07f-b0edb6050714': '%7B%22g%22%3A%22468792084%22%2C%22c%22%3A1741687301673%2C%22l%22%3A1741787396469%7D',
#     'ab.storage.sessionId.4e505175-14eb-44b5-b07f-b0edb6050714': '%7B%22g%22%3A%22d4010e47-2ace-7dbb-7bad-5ab46cdb38c4%22%2C%22e%22%3A1741789214065%2C%22c%22%3A1741787396469%2C%22l%22%3A1741787414065%7D',
#     '__Host-NEXT_MEETUP_CSRF': '7d1b5f20-5257-4602-b22d-ba2ce26414da',
#     'SIFT_SESSION_ID': '6a121aa2-227b-4576-a908-b8354d460785',
#     'MEETUP_CSRF': '8bb727d3-95f5-4103-8295-08be95e4c5fc',
#     'enable_fundraising_pledge_banner_show': 'true',
#     'MEETUP_MEMBER_LOCATION': '__typename=LocationSearch&city=Delhi&country=in&lat=28.670000076293945&lon=77.20999908447266&name=Delhi%252C+India%252C+meetup2&state=&timeZone=Asia%252FKolkata&borough=&localizedCountryName=in&neighborhood=&zip=meetup2',
#     '__stripe_sid': '85b0f2ca-d560-4b31-af5d-dacde59976c5486eb6',
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
#     'Accept': '*/*',
#     'Accept-Language': 'en-US',
#     # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Referer': 'https://www.meetup.com/groups/',
#     'content-type': 'application/json',
#     'apollographql-client-name': 'nextjs-web',
#     'x-meetup-view-id': 'dab72e4a-3300-4a87-9630-63609d7ce2e0',
#     'sentry-trace': '377c4da50e324840bedae12a43550c0d-bf705777efb16e2f-0',
#     'baggage': 'sentry-environment=production,sentry-release=2d3edfbfb2af0c3264e8558b596218880e27bb5b,sentry-public_key=5d12cd2317664353456ab4c40d079af2,sentry-trace_id=377c4da50e324840bedae12a43550c0d,sentry-sample_rate=0.1,sentry-transaction=%2Fgroups,sentry-sampled=false',
#     'Origin': 'https://www.meetup.com',
#     'Connection': 'keep-alive',
#     # 'Cookie': 'MEETUP_BROWSER_ID=id=03593dbe-960c-4b7b-9ea2-ab580e92a4cc; MEETUP_TRACK=id=2c23958b-d6c3-4fe1-ac48-1bd0effa2092; LOGGED_OUT_HOMEPAGE_SEGMENTATION=spotlight_hero_social_proof; __stripe_mid=daa18f66-e96d-4d0e-a32b-52474e1c5ecb2317b6; memberId=468792084; isSpooner=false; MEETUP_SESSION=bc184049-375c-42a8-b7a3-5e9d63dfaca1; __meetup_auth_access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0Njg3OTIwODQiLCJuYmYiOjE3NDE2ODczMDAsInJvbGUiOiJmaXJzdF9wYXJ0eSIsImlzcyI6Ii5tZWV0dXAuY29tIiwicXVhbnR1bV9sZWFwZWQiOmZhbHNlLCJyZWZyZXNoX3Rva2Vuc19jaGFpbl9pZCI6IjczYTU0NzgyLTRiYjAtNDE1OS04NjBlLWIxZDc3YWI0ZTBlMCIsImV4cCI6MTc0MTY5MDkwMCwiaWF0IjoxNzQxNjg3MzAwLCJqdGkiOiI0ZjZlM2IwYS1lNGUzLTQzOTMtOTAwYi03MmM3NjMzYWUyYjUifQ.htNbt38JrUIh1EsMoAYeVK1yNTLOWiYnAwu1_He0XXk4R2YWcksj4zvdJG8CJ9sVcm_sS4MzoVWIwn1xNVXaSA; ab.storage.deviceId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%22f3bea9e6-d37b-0a33-d612-ac4f9bfb65dc%22%2C%22c%22%3A1741687301663%2C%22l%22%3A1741787396469%7D; ab.storage.userId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%22468792084%22%2C%22c%22%3A1741687301673%2C%22l%22%3A1741787396469%7D; ab.storage.sessionId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%22d4010e47-2ace-7dbb-7bad-5ab46cdb38c4%22%2C%22e%22%3A1741789214065%2C%22c%22%3A1741787396469%2C%22l%22%3A1741787414065%7D; __Host-NEXT_MEETUP_CSRF=7d1b5f20-5257-4602-b22d-ba2ce26414da; SIFT_SESSION_ID=6a121aa2-227b-4576-a908-b8354d460785; MEETUP_CSRF=8bb727d3-95f5-4103-8295-08be95e4c5fc; enable_fundraising_pledge_banner_show=true; MEETUP_MEMBER_LOCATION=__typename=LocationSearch&city=Delhi&country=in&lat=28.670000076293945&lon=77.20999908447266&name=Delhi%252C+India%252C+meetup2&state=&timeZone=Asia%252FKolkata&borough=&localizedCountryName=in&neighborhood=&zip=meetup2; __stripe_sid=85b0f2ca-d560-4b31-af5d-dacde59976c5486eb6',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'Priority': 'u=4',
#     # Requests doesn't support trailers
#     # 'TE': 'trailers',
# }

# json_data = {
#     'operationName': 'getSelfActiveGroups',
#     'variables': {
#         'first': 20,
#     },
#     'extensions': {
#         'persistedQuery': {
#             'version': 1,
#             'sha256Hash': '40c4a04c8466f43b2b5719d8b7b8107b2f333b8b503a503b3ad43c7e41fb6b42',
#         },
#     },
# }

# response = requests.post('https://www.meetup.com/gql2', cookies=cookies, headers=headers, json=json_data)

# for edge in response.json()['data']['self']['memberships']['edges']:
#     group = Group.from_json(edge['node'])
#     print(group)

# import requests

# cookies = {
#     'MEETUP_BROWSER_ID': 'id=03593dbe-960c-4b7b-9ea2-ab580e92a4cc',
#     'MEETUP_TRACK': 'id=2c23958b-d6c3-4fe1-ac48-1bd0effa2092',
#     'LOGGED_OUT_HOMEPAGE_SEGMENTATION': 'spotlight_hero_social_proof',
#     '__stripe_mid': 'daa18f66-e96d-4d0e-a32b-52474e1c5ecb2317b6',
#     'memberId': '468792084',
#     'isSpooner': 'false',
#     'MEETUP_SESSION': 'bc184049-375c-42a8-b7a3-5e9d63dfaca1',
#     '__meetup_auth_access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0Njg3OTIwODQiLCJuYmYiOjE3NDE2ODczMDAsInJvbGUiOiJmaXJzdF9wYXJ0eSIsImlzcyI6Ii5tZWV0dXAuY29tIiwicXVhbnR1bV9sZWFwZWQiOmZhbHNlLCJyZWZyZXNoX3Rva2Vuc19jaGFpbl9pZCI6IjczYTU0NzgyLTRiYjAtNDE1OS04NjBlLWIxZDc3YWI0ZTBlMCIsImV4cCI6MTc0MTY5MDkwMCwiaWF0IjoxNzQxNjg3MzAwLCJqdGkiOiI0ZjZlM2IwYS1lNGUzLTQzOTMtOTAwYi03MmM3NjMzYWUyYjUifQ.htNbt38JrUIh1EsMoAYeVK1yNTLOWiYnAwu1_He0XXk4R2YWcksj4zvdJG8CJ9sVcm_sS4MzoVWIwn1xNVXaSA',
#     'ab.storage.deviceId.4e505175-14eb-44b5-b07f-b0edb6050714': '%7B%22g%22%3A%22f3bea9e6-d37b-0a33-d612-ac4f9bfb65dc%22%2C%22c%22%3A1741687301663%2C%22l%22%3A1741790351609%7D',
#     'ab.storage.userId.4e505175-14eb-44b5-b07f-b0edb6050714': '%7B%22g%22%3A%22468792084%22%2C%22c%22%3A1741687301673%2C%22l%22%3A1741790351609%7D',
#     'ab.storage.sessionId.4e505175-14eb-44b5-b07f-b0edb6050714': '%7B%22g%22%3A%221e77efe4-e84e-0a2b-04e2-a84a00c547c5%22%2C%22e%22%3A1741792151608%2C%22c%22%3A1741790351608%2C%22l%22%3A1741790351608%7D',
#     '__Host-NEXT_MEETUP_CSRF': '1882f4a6-22e2-4f0f-a2dc-dde268477c6a',
#     'SIFT_SESSION_ID': '6a121aa2-227b-4576-a908-b8354d460785',
#     'MEETUP_CSRF': '8bb727d3-95f5-4103-8295-08be95e4c5fc',
#     'enable_fundraising_pledge_banner_show': 'true',
#     'MEETUP_MEMBER_LOCATION': '__typename=LocationSearch&city=Delhi&country=in&lat=28.670000076293945&lon=77.20999908447266&name=Delhi%252C+India%252C+meetup2&state=&timeZone=Asia%252FKolkata&borough=&localizedCountryName=in&neighborhood=&zip=meetup2',
#     '__stripe_sid': '85b0f2ca-d560-4b31-af5d-dacde59976c5486eb6',
#     'USER_CHANGED_DISTANCE_FILTER': 'false',
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     # 'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Referer': 'https://www.meetup.com/groups/',
#     'Connection': 'keep-alive',
#     # 'Cookie': 'MEETUP_BROWSER_ID=id=03593dbe-960c-4b7b-9ea2-ab580e92a4cc; MEETUP_TRACK=id=2c23958b-d6c3-4fe1-ac48-1bd0effa2092; LOGGED_OUT_HOMEPAGE_SEGMENTATION=spotlight_hero_social_proof; __stripe_mid=daa18f66-e96d-4d0e-a32b-52474e1c5ecb2317b6; memberId=468792084; isSpooner=false; MEETUP_SESSION=bc184049-375c-42a8-b7a3-5e9d63dfaca1; __meetup_auth_access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0Njg3OTIwODQiLCJuYmYiOjE3NDE2ODczMDAsInJvbGUiOiJmaXJzdF9wYXJ0eSIsImlzcyI6Ii5tZWV0dXAuY29tIiwicXVhbnR1bV9sZWFwZWQiOmZhbHNlLCJyZWZyZXNoX3Rva2Vuc19jaGFpbl9pZCI6IjczYTU0NzgyLTRiYjAtNDE1OS04NjBlLWIxZDc3YWI0ZTBlMCIsImV4cCI6MTc0MTY5MDkwMCwiaWF0IjoxNzQxNjg3MzAwLCJqdGkiOiI0ZjZlM2IwYS1lNGUzLTQzOTMtOTAwYi03MmM3NjMzYWUyYjUifQ.htNbt38JrUIh1EsMoAYeVK1yNTLOWiYnAwu1_He0XXk4R2YWcksj4zvdJG8CJ9sVcm_sS4MzoVWIwn1xNVXaSA; ab.storage.deviceId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%22f3bea9e6-d37b-0a33-d612-ac4f9bfb65dc%22%2C%22c%22%3A1741687301663%2C%22l%22%3A1741790351609%7D; ab.storage.userId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%22468792084%22%2C%22c%22%3A1741687301673%2C%22l%22%3A1741790351609%7D; ab.storage.sessionId.4e505175-14eb-44b5-b07f-b0edb6050714=%7B%22g%22%3A%221e77efe4-e84e-0a2b-04e2-a84a00c547c5%22%2C%22e%22%3A1741792151608%2C%22c%22%3A1741790351608%2C%22l%22%3A1741790351608%7D; __Host-NEXT_MEETUP_CSRF=1882f4a6-22e2-4f0f-a2dc-dde268477c6a; SIFT_SESSION_ID=6a121aa2-227b-4576-a908-b8354d460785; MEETUP_CSRF=8bb727d3-95f5-4103-8295-08be95e4c5fc; enable_fundraising_pledge_banner_show=true; MEETUP_MEMBER_LOCATION=__typename=LocationSearch&city=Delhi&country=in&lat=28.670000076293945&lon=77.20999908447266&name=Delhi%252C+India%252C+meetup2&state=&timeZone=Asia%252FKolkata&borough=&localizedCountryName=in&neighborhood=&zip=meetup2; __stripe_sid=85b0f2ca-d560-4b31-af5d-dacde59976c5486eb6; USER_CHANGED_DISTANCE_FILTER=false',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Priority': 'u=0, i',
#     # Requests doesn't support trailers
#     # 'TE': 'trailers',
# }

# params = {
#     'eventOrigin': 'your_groups',
# }

# response = requests.get(
#     'https://www.meetup.com/central-delhi-toastmasters-club-cdtm/',
#     params=params,
#     cookies=cookies,
#     headers=headers,
# )

# print(response.text)

from queries.groups_query import GroupsQuery, GroupQueryParams
from queries.group_events_query import GroupEventsQuery, GroupEventsQueryParams

client = Client()

# cookiesRes = client.getBaseCookies()
# cookies = cookiesRes.cookies
# headers = client.getHeaders(browser=cookiesRes.browser)

groupQuery = GroupEventsQuery(extraHeaders={}, extraCookies={}, params=GroupEventsQueryParams(groupName="travelingsoulsdotorg"))
client.executeQuery(query=groupQuery)
