import requests
import json

# attempting to get data via network request, but failing
# this request works with curl and directly in the browser, but getting
# an empty response back when trying with the python.requests module
# response status is 200 OK, just no data
KOM_SPRINT_URL = 'https://www.zwiftpower.com/api3.php?do=event_sprints&zid=1471415&_=1610548857933'
RESULTS_URL = 'https://www.zwiftpower.com/cache3/results/1471415_zwift.json?_=1610548964682'
kom_and_sprint_result = requests.get(
    KOM_SPRINT_URL,
    headers={
        'accept': 'application/json',
        'authority': 'zwiftpower.com'
    }
)
STAGE_2_KOM_AND_SPRINT_DATA = kom_and_sprint_result.text
STAGE_2_RESULTS_DATA = requests.get(RESULTS_URL, headers={'content-type': 'application/json'})
