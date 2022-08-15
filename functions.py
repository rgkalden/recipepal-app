import streamlit as st
import numpy as np
import pandas as pd

# Functions


@st.cache()
def loadRawData(filename, nrows=200):
    '''
    Function to load raw data into a pandas dataframe

    Parameters:
    filename - name of parquet file
    nrows - number of first rows to be taken from file into dataframe

    Returns: pandas dataframe
    '''
    return pd.read_parquet(filename)[:nrows]


def selectColumns(dataframe, columns):
    '''
    Function to select columns from dataframe

    Parameters:
    dataframe - dataframe
    columns - columns to select

    Returns: pandas dataframe
    '''
    newDataframe = dataframe.copy()
    return newDataframe[columns]


def convertTimes(dataframe, columns):
    '''
    Function to convert ISO8601 format time durations into minutes

    Parameters:
    dataframe - dataframe
    columns - columns containing ISO8601 time durations

    Returns:
    None - (dataframe modified in place)
    '''
    for column in columns:
        dataframe[column] = pd.to_timedelta(
            dataframe[column], errors='coerce') / np.timedelta64(1, 'm')


def removeNullValues(dataframe):
    '''
    Function to drop null values from rows in dataframe
    '''
    dataframe.dropna(axis=0, inplace=True)


def to_1D(series):
    '''
    Function to turn a pandas series of lists (eg 2D) 
    into a single series containing all values (1D)

    Parameters:
    series - series containing values that are of list type

    Returns:
    pandas series containing all values in the original series
    '''
    return pd.Series([x for _list in series for x in _list])


def searchItem(dataframe, column, target, mode='or'):
    '''
    Function to search for a value within a dataframe column.
    Column contains values that are lists.

    Parameters:
    dataframe - dataframe
    column - column containing values that are lists.
    target - List of one or more search terms
    mode - 'or' search (default), 'and' search

    Returns:
    foundIndex - list of indices where search terms have been found.
                 can be subsequently used to filter a dataframe
    '''
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
    '''
    Function to display the number of recipes (length) of a dataframe

    Parameters:
    dataframe - dataframe

    Returns:
    None (output is written to app)
    '''
    if len(dataframe) == 0:
        st.write('No recipes found')
    else:
        st.write(len(dataframe), " recipes found")