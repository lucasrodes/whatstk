def preprocess(dataframe):
    # Center each dimension
    dataframe = dataframe.sub(dataframe.mean(axis=1), axis=0)
    # Normalize each dimension
    dataframe = dataframe.divide(
        dataframe.max(axis=1) - dataframe.min(axis=1), axis=0)
    # Show dataframe
    return dataframe