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

## Stage Results
You can view the results in the above `results` directory

Running the `get results.py` script will process the data stored in the `zp_data` directory compare it to our registration data in the `veganuary_data` directory (currently only for stages 1 and 2) and produce results stored in the `results` directory. Stage results are broken down by category, while prime results are broken down by the prime name and category (i.e. `veganuary_prime_results_c_Marina_Sprint.csv`. At first glance they appear to be accurate, but I haven't combed through them super thoroughly so let me know if you see any errors!

Prime results have the womens results at the end (identified by the gender column having a value of 2)

## Overall Standings
I have input the latest data as CSVs in the `veganuary_data/standings` directory.

Next:
- Use the current overall standings and the stage results to calculate new overall standings

# Getting Results After a New Stage
## Get Stage Data From ZwiftPower
- To get the results data, open the chrome dev tools inspector (right click, inspect), go to the network tab and search for a network request ending in `_zwift.json` (something like `1471415_zwift.json?_=1610371372960`). Right click on that request and click `copy response`
- Create a new file under the `zp_data/stage_n` directory (you will have to create this directory) and name it `stage_n_results.py`
- Create a new variable and paste the copied data into a multiline string:
  ```
  STAGE_4_RESULTS = '''pasted data goes here'''
  ```
- Go back to ZwiftPower and go to the primes tab, select a category and select "fastest time"
- Look in the networks tab for a network request that should be something like `api3.php?do=event_primes...` and copy the data from that request.
- Create a new file and variable for that data as well, something like `STAGE_2_PRIME_DATA_C`
## Create a New Results Directory
- Add a new directory in the `results` folder and name it `stage_n` (replace `n` with the stage number)
## Modify the get_results.py file
- Import your result data into `get_results.py` like this:
  ```
  # import stage 1 data
  from zp_data.stage_1.stage_1_results import STAGE_1_RESULTS
  from zp_data.stage_1.stage_1_prime_a import STAGE_1_PRIME_DATA_A
  from zp_data.stage_1.stage_1_prime_b import STAGE_1_PRIME_DATA_B
  from zp_data.stage_1.stage_1_prime_c import STAGE_1_PRIME_DATA_C
  from zp_data.stage_1.stage_1_prime_d import STAGE_1_PRIME_DATA_D
  ```
- Instantiate a new `StageResultsModel` with your stage results:
  ```
  # Run script for stage 1
  stage_1_model = StageResultsModel(STAGE_1_RESULTS)
  ```
- Call the `get_veganuary_stage_results()` with the following arguments and print a statement:
  - category
  - stage_number
  ```
  # stage results by cat
  stage_1_model.get_veganuary_stage_results("a", 1)
  print("resolving stage results for cat A")
  stage_1_model.get_veganuary_stage_results("b", 1)
  print("resolving stage results for cat B")
  stage_1_model.get_veganuary_stage_results("c", 1)
  print("resolving stage results for cat C")
  stage_1_model.get_veganuary_stage_results("d", 1)
  print("resolving stage results for cat D")
  ```
- Call the `get_veganuary_prime_results()` method with the following arguments and print a statement:
  - prime_data
  - category
  - stage_number
  ```
  # prime results by cat
  stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_A, "a", 1)
  print("resolving prime results for cat A")
  stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_B, "b", 1)
  print("resolving prime results for cat B")
  stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_C, "c", 1)
  print("resolving prime results for cat C")
  stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_D, "d", 1)
  print("resolving prime results for cat D")
  ```
## Run the Script
- Run the script and check that results were populated in your new stage directory under the `results` directory.
