import pandas as pd
import glob
import json

files = glob.glob(r"D:\DATA SCIENCE\Exception_Handling\json_files\*.json")

dfs = []
for f in files:
    with open(f, "r") as json_file:
        data = json.load(json_file)  
        try:
            df = pd.DataFrame(data)   
        except ValueError:
            df = pd.json_normalize(data) 

        dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

print(final_df)
