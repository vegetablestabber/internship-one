from pandas import DataFrame

def insert_levels(df: DataFrame):
    """Insert a column for the levels of an industry classification standard.

    Args:
        df (DataFrame): Inference DataFrame for an industry classification standard.
    """

    levels = df.index.str.len()
    df.insert(0, "Level", levels)

def insert_parents(df: DataFrame):
    """Insert a column for the parents of an industry classification standard.

    Args:
        df (DataFrame): Inference DataFrame for an industry classification standard.
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

def default_clean(df: DataFrame):
    """Simple text cleaning for industry classification standard inference DataFrames.

    Args:
        df (DataFrame): Inference DataFrame for an industry classification standard.
    """

    # Normalisation (lowercase strings)
    # lower = lambda x: x.lower() if isinstance(x, str) else x
    
    ## If the dataframe has ISIC code data
    # if "ISIC code" in df:
    #     if "Parent" in df:
    #         df.iloc[:, 2:-1] = df.iloc[:, 2:-1].map(lower)
    #     else:
    #         df.iloc[:, 1:-1] = df.iloc[:, 1:-1].map(lower)
        
    ## If the dataframe doesnt' have ISIC code data
    # else:
    #     df.loc[:, "Description":] = df.loc[:, "Description":].map(lower)
    
    # Replace punctuation with empty strings
    # df.loc[:, "Description":] = df.loc[:, "Description":].replace(r"[^\w\s]+", " ", regex=True)
    
    # Replace newlines and multiple spaces with whitespaces
    # df.replace([r"\n", r" +"], " ", regex=True, inplace=True)
    
    # Remove leading and trailing whitespaces
    df.loc[:, "Description":] = df.loc[:, "Description":].map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Replace 'and or' with 'or'
    df.replace(r"and/or", "or", regex=True, inplace=True)