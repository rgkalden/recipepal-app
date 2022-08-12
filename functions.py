import streamlit as st
import numpy as np
import pandas as pd

# Functions


@st.cache()
def loadRawData(filename, nrows):
    return pd.read_parquet(filename)[:nrows]


def selectColumns(dataframe, columns):
    newDataframe = dataframe.copy()
    return newDataframe[columns]


def convertTimes(dataframe, columns):
    for column in columns:
        dataframe[column] = pd.to_timedelta(
            dataframe[column], errors='coerce') / np.timedelta64(1, 'm')


def removeNullValues(dataframe):
    dataframe.dropna(axis=0, inplace=True)


def to_1D(series):
        return pd.Series([x for _list in series for x in _list])


def searchItem(dataframe, column, target, mode='or'):
    series = dataframe[column].to_list()

    # OR Search
    if mode == 'or':
        foundIndex = []
        for targetValue in target:
            for i in range(0, len(series)):
                for item in series[i]:
                    if item == targetValue:
                        foundIndex.append(i)

        return list(set(foundIndex))

    # AND Search
    elif mode == 'and':
        foundIndex = []
        for i in range(0, len(series)):
                for item in series[i]:
                    check = all(item in series[i] for item in target)
                    #if item in target:
                    if check:
                        foundIndex.append(i)

        return list(set(foundIndex))

def displayNumberOfRecipes(dataframe):
    if len(dataframe) == 0:
        st.write('No recipes found')
    else:
        st.write(len(dataframe), " recipes found")