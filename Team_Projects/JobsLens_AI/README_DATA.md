# Data Setup Instructions

## Missing Data File

The modeling script requires the `join_dataset.xlsx` file which is not currently in the repository.

## Required Files

1. ✅ `hai_full_database.csv` - **Present** in `Team_Projects/JobsLens_AI/data/`
2. ❌ `join_dataset.xlsx` - **MISSING** - needs to be added

## How to Add the Missing File

You need to place the `join_dataset.xlsx` file in:
```
Team_Projects/JobsLens_AI/data/join_dataset.xlsx
```

## Where to Get the File

The JOIN dataset should be downloaded from the World Bank Global Labor Database.

Sources mentioned in the challenge:
- **Data360 (Labor Force Surveys)**
- **World Bank Global Labor Database**
- **WBG Global Jobs Indicators Database**

## Once You Have the File

1. Place it in `Team_Projects/JobsLens_AI/data/join_dataset.xlsx`
2. Run the model:
   ```bash
   cd /Users/rafaelkovashikawa/Downloads/projects/DataDive25
   bash Team_Projects/JobsLens_AI/run_model.sh
   ```

## Alternative: Update the Script Path

If your `join_dataset.xlsx` is in a different location, update line 437 in:
`Team_Projects/JobsLens_AI/src/model_ai_jobs.py`

Change:
```python
join_dataset = pd.read_excel('Team_Projects/JobsLens_AI/data/join_dataset.xlsx')
```

To point to your actual file location.
