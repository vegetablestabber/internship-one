from pandas import DataFrame

def insert_levels(df: DataFrame):
    """Insert a column for the levels of a classification standard.

    Args:
        df (DataFrame): Inference DataFrame for a classification standard.
    """

    levels = df.index.str.len()
    df.insert(0, "Level", levels)

def insert_parents(df: DataFrame):
    """Insert a column for the parents of a classification standard.

    Args:
        df (DataFrame): Inference DataFrame for a classification standard.
    """

    parents = []
    history = []
    prev = {"Level": 0, "Code": ""}

    # Iterate through the dataframe to deduce the parent
    for row in df.itertuples():
        prev_level = len(history)
        current_level = row.Level
        current_code = row.Index
        
        ## If the current level is '1'
        if current_level == 1:
            current_parent = ""
            history = [current_code]
            
        ## If the current level is lower than the previous level
        elif current_level > prev_level:
            current_parent = history[prev_level - 1]
            history.append(current_code)
            
        ## If the current level is higher than the previous level
        elif current_level < prev_level:
            current_parent = history[(current_level - 1) - 1]
            del history[current_level - 1:]
            history.append(current_code)
        
        else:
            current_parent = history[(current_level - 1) - 1]
        
        parents.append(current_parent)
        prev.update({"Level": current_level, "Code": current_code})
        
    # Insert the list as a column
    df.insert(1, "Parent", parents)