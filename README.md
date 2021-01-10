# veganuary

A Python script that could help automate the process of calculating results for Team Vegan's Veganuary Race League

To run the script open terminal (for mac) and type
```
python3 get_results.py
```

You should see something like:
```
Number of A Riders: 101
Number of A Rider Rsults: 121
Number of valid riders for A cat: 8
```

That's as far as I've got. Next steps should be something like:
- Include the riders ZP number in the CSV so we can validate against that instead of name.
- Filter existing results down to only validated riders (including sprint/kom etc.)
- Out put filtered stage results
- Have a way to input most current overall results into the `CalculateResults` class (create csv?)
- Update overall results based on stage results
- Export as csv
