import requests
import json

# attempting to get data via network request, but failing
# this request works with curl and directly in the browser, but getting
# an empty response back when trying with the python.requests module
# response status is 200 OK, just no data
KOM_SPRINT_URL = 'https://www.zwiftpower.com/api3.php'
data = {
    "do": "event_sprints",
    "zid": "1471415",
    "_": "1610548857933"
}
RESULTS_URL = 'https://www.zwiftpower.com/cache3/results/1471415_zwift.json?_=1610548964682'
kom_and_sprint_result = requests.get(
    KOM_SPRINT_URL,
    headers = {
        "accept": "accept: application/json",
        "accept-encoding": "gzip, deflate, br",
        "dnt": "1",
        "authority": "zwiftpower.com",
        "referer": "https://zwiftpower.com/events.php?zid=1471415"

    },
    json=data
)
STAGE_2_KOM_AND_SPRINT_DATA = kom_and_sprint_result.text
GET_STAGE_2_DATA = requests.get(RESULTS_URL)
