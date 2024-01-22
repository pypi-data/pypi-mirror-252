# Topsis-102103596
Library for calculating topsis score and rank for a Multi Criteria Decision Making problem.

## Usage
#### Installation
```sh
pip install topsis-102103596
```

#### Usage
Contains a single function
**cal_topsis_score(df,w,i,out_file):**

where:

    df -> pd.DataFrame

    w -> list of weights (only numeric columns are considered, rest are ignored)

    i -> impact list ("+" for columns that are to be maximized, "-" for columns to be minimized, for example ["-","+","+","+"])

    out_file -> csv file in which output Dataset will be stored
    
#### Screenshots
Input file: data.csv

![Data.csv](images/data.png)

Output file: out.csv

![Output.csv](images/out.png)
