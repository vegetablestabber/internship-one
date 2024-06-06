from pathlib import Path 
from pandas import read_csv, read_excel

from utils.constants import FILENAMES

def import_data():
    dfs = dict()
    
    for std, paths in FILENAMES["data"].items():
        dfs[std] = []
        
        for path in paths:
            if type(path) == str:
                if ".xls" in path:
                    dfs[std].append(read_excel(path))
                elif ".csv" in path:
                    dfs[std].append(read_csv(path))
            elif type(path) == tuple:
                if ".xls" in path[0]:
                    dfs[std].append(read_excel(path[0], sheet_name=path[1]))
    
    return dfs

# Save data to new CSV files
def export_dfs(d):
    for std, df in d.items():
        filepath = Path(FILENAMES["exports"][std])  
        filepath.parent.mkdir(parents=True, exist_ok=True)  

        df.to_csv(filepath)