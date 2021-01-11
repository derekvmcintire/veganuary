# veganuary
A Python script that could help automate the process of calculating results for Team Vegan's Veganuary Race League

Clone this repo and then you can:

run the script - open terminal (for mac) and type
```
python3 get_results.py
```

You should see something like:
```
resolving stage results for cat A
resolving stage results for cat B
resolving stage results for cat C
resolving stage results for cat D
resolving prime results for cat A
resolving prime results for cat B
resolving prime results for cat C
resolving prime results for cat D

```
## Results
You can view the results in the above `results` directory and download them by right clicking on the file in the list view and selecting "Save File As"

Running the `get results.py` script will process the data stored in the `zp_data` directory (currently only for stage 2) and produce results stored in the `results` directory. Stage results are broken down by category, while prime results are broken down by the prime name and category. At first glance they appear to be accurate, but I haven't combed through them super thoroughly so let me know if you see any errors!

Next:
- Have a way to input most current overall results into the `CalculateResults` class
- Update overall results based on stage results

## To get data from ZP
- There may be a better way of doing this but I didn't see a public API in my quick search

To get the results data I went to Zwift Power, opened the chrome dev tools inspector, went to the network tab and found a network request ending in .json: `1471415_zwift.json?_=1610371372960` - but you should be able to view it here: https://zwiftpower.com/cache3/results/1471415_zwift.json?_=1610371372960
Note:
- These results have NOT been filtered for UPG/HR/WKG from what I can tell
- I believe the "label" key is used for category cat A = lable: 1, cat B = label: 2 etc.
- For prime data, you need to select the category and "fastest time" and get data separately for each category
