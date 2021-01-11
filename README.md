# veganuary
*UPDATED*: Got zwift IDs working, but had to grab data from the `_ziwft.json` network request instead. It's a little less clear, but details below.

A Python script that could help automate the process of calculating results for Team Vegan's Veganuary Race League

Clone this repo and then you can:

To run the script open terminal (for mac) and type
```
python3 get_results.py
```

You should see something like:
```
Number of A Riders: 103
Number of valid A Rider Rsults: 64
Number of B Riders: 124
Number of valid B Rider Rsults: 73
Number of C Riders: 101
Number of valid C Rider Rsults: 62
Number of D Riders: 45
Number of valid D Rider Rsults: 29
➜  veganuary git:(dumb) ✗ 

```

So it currently filters out riders that are not registered for the league.

That's as far as I've got. Next steps should be something like:
- Include the riders ZP number in the CSV so we can validate against that instead of name.
- Filter existing results down to only validated riders
- Out put filtered stage results
- Will need to input sprint and KOM data separately and write methods to hanlde filtering
- Output filtered results as csv (mocked the methods but untested)

Then:
- Have a way to input most current overall results into the `CalculateResults` class (create csv?)
- Update overall results based on stage results
- Export as csv

## To get data from ZP
- There may be a better way of doing this but I didn't see a public API in my quick search

To get the results data I went to Zwift Power, opened the chrome dev tools inspector, went to the network tab and found a network request ending in .json: `1471415_zwift.json?_=1610371372960` - but you should be able to view it here: https://zwiftpower.com/cache3/results/1471415_zwift.json?_=1610371372960
Note:
- These results have NOT been filtered for UPG/HR/WKG from what I can tell
- I believe the "label" key is used for category cat A = lable: 1, cat B = label: 2 etc.
