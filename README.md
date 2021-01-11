# veganuary

A Python script that could help automate the process of calculating results for Team Vegan's Veganuary Race League

To run the script open terminal (for mac) and type
```
python3 get_results.py
```

You should see something like:
```
This aint gonna work until we get those ZIDs
```

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

To get the results data I went to Zwift Power, opened the chrome dev tools inspector, went to the network tab and found a network request ending in .json: `1471415_view.json?_=1610320600772` - but you should be able to view it here: https://zwiftpower.com/cache3/results/1471415_view.json?_=1610320600772
Note these results only include what loads on the page - so they have already been filtered for UPG/HR/WKG etc. and this data does not include the Sprint/KOM/QOM data
