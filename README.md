# veganuary

## Latest Updates
- I was having trouble getting all of the prime data since the "primes" tab in ZP only receives data from the top 10 fastest time on each lap, and if there are a lot of unregistered riders in the top 10, that would sometimes leave less than 10 registered riders with data for their times.
- I was able to find full result data under the "Sprints and KOMs" tab - so I re-wrote the algorithm that calculates prime results and got it working perfectly for stage 2!
- Problem is that "Sprints and KOMs" tab and the data that comes with it doesn't seem to exist for every race, and stage 1 doesn't have it. So now I have no way to calculate prime data for stage 1 - unless I add the old algorithm back in. I'll do it, but it will only give me partial results. I'm not sure if ZP is having issues or of Chris  got the prime data for stage 1 a different way.


A Python script that could help automate the process of calculating results for Team Vegan's Veganuary Race League

Clone this repo and then you can:

run the script - open terminal (for mac) and type
```
python3 get_results.py
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
➜  veganuary git:(main) ✗ 

```

## Results
You can view the results in the above `results` directory

Running the `run_script.py` script fetch data for results and primes from zwift power - this can take a few seconds. It then produce results stored in the `results` directory. Stage results are broken down by category, while prime results are broken down by the prime ID and category (i.e. `veganuary_prime_results_c_47.csv`. At first glance they appear to be accurate, but I haven't combed through them super thoroughly so let me know if you see any errors! Note: Prime results are not split by gender yet.

## Overall Standings
I have input the latest data as CSVs in the `veganuary_data/standings` directory.

Next:
- Split primes by gender
- Use the current overall standings and the stage results to calculate new overall standings

# Getting Results After a New Stage
- Get the Zwift Power Event ID
- Get the sprint and kom IDs

## Modify the get_results.py file
*Update This* since this has changged now - it is much simpler!
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
