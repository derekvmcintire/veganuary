# veganuary
A Python script that could help automate the process of calculating results for Team Vegan's Veganuary Race League

## Overall Standings
I have input the latest data as CSVs in the `veganuary_data/standings` directory, but there are no calculations for overall standings yet.

## Viewing Results
- Click on the `results` directory above to find results sorted by stage.
- Stage results can be found separated by category in the following format: `stage_[stage number]_results_[category].csv` i.e. `stage_1_results_a.csv`
- Prime results can be found separated by category in the following format: `[gender]_prime_results_[category]_[prime name]` i.e. `w_prime_results_b_54.csv`
#### Notes on Primes
- Points are configurable, I'm not 100% on which primes were used and which ones were worth how many points, so I made my best guess - you can see which ones I passed in to each stage in the `run_script.py` file
- Primes are only showing by their ID number for now since it's an extra network request to get their names, I can add that later
- I added sprint points for both current stages on the finish line. This is also configurable and the name of the prime is `finish` and they are not sorted by gender (yet!), so the file names start with `a` i.e. `a_prime_results_c_finish.csv`

# Getting Results After a New Stage
- To start, you will need to have git set up locally, clone this repo and have python3 running on your machine, then:

- Get the Zwift Power Event ID
- Get the sprint and kom IDs

## Modify the get_results.py file
- Step 1 - create a new instance of `StageModel` and pass it:
  - the Zwift Power Event ID (int) i.e. `12345656`
  - A list of sprint IDs (list) i.e. ```[`54`, `61`, `63`]```
  - A list of K/QOM IDs (list) i.e. ```[`33`, `21`]```
  - [OPTIONAL]: point system to use for sprints (list) i.e. `[20, 15, 10, 8, 6, 5, 4, 3, 2, 1]`
  - [OPTIONAL]: point system to use for K/QOMs (list) i.e. `[12, 10, 8, 7, 6, 5, 4, 3, 2, 1]`
  - [OPTIONAL]: the finishing sprint flag (bool) i.e. `True`
  - [OPTIONAL]: if finishing sprint flat is `True` you must provide a points system (list) i.e. `[20, 15, 10, 8, 6, 5, 4, 3, 2, 1]`
```
# ==========================================================#
# ================ Run script for stage 2 ==================#
# ==========================================================#
  print('Fetching data for stage 2...')
  stage_2 = StageModel(
  STAGE_2_EVENT_ID, // 12345656
  stage_2_sprints, // [`54`, `61`, `63`]
  stage_2_koms, // [`33`, `21`]
  SINGLE_POINTS, // [20, 15, 10, 8, 6, 5, 4, 3, 2, 1]
  DOUBLE_POINTS, // [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
  True, // True
  DOUBLE_POINTS // [20, 15, 10, 8, 6, 5, 4, 3, 2, 1]
  )
  stage_2.print_stage_results('a', 2)
  print('Exporting Cat A results for stage 2')
  stage_2.print_stage_results('b', 2)
  print('Exporting Cat B results for stage 2')
  stage_2.print_stage_results('c', 2)
  print('Exporting Cat C results for stage 2')
  stage_2.print_stage_results('d', 2)
  print('Exporting Cat D results for stage 2')
  stage_2.print_prime_results('a', 2)
  print('Exporting Cat A sprint and KOM results for stage 2')
  stage_2.print_prime_results('b', 2)
  print('Exporting Cat B sprint and KOM results for stage 2')
  stage_2.print_prime_results('c', 2)
  print('Exporting Cat C sprint and KOM results for stage 2')
  stage_2.print_prime_results('d', 2)
  print('Exporting Cat D sprint and KOM results for stage 2')
  print('Done!')
```

## Run the script
run the script - open terminal (for mac) and type
```
python3 run_script.py
```

You should see something like:
```
➜  veganuary git:(main) ✗ python3 run_script.py
Fetching data for stage 1...
Exporting Cat A results for stage 1
Exporting Cat B results for stage 1
Exporting Cat C results for stage 1
Exporting Cat D results for stage 1
Exporting Cat A sprint and KOM results for stage 1
Exporting Cat B sprint and KOM results for stage 1
Exporting Cat C sprint and KOM results for stage 1
Exporting Cat D sprint and KOM results for stage 1
Done!
Fetching data for stage 2...
Exporting Cat A results for stage 2
Exporting Cat B results for stage 2
Exporting Cat C results for stage 2
Exporting Cat D results for stage 2
Exporting Cat A sprint and KOM results for stage 2
Exporting Cat B sprint and KOM results for stage 2
Exporting Cat C sprint and KOM results for stage 2
Exporting Cat D sprint and KOM results for stage 2
Done!
```
