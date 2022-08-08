import streamlit as st
import numpy as np
import pandas as pd

st.title("RecipePal")

@st.cache()
def loadRawData(filename, nrows):
    return pd.read_csv(filename, nrows=nrows)


def selectColumns(dataframe, columns):
    newDataframe = dataframe.copy()
    return newDataframe[columns]


def removeNullValues(dataframe):
    dataframe.dropna(axis=0, inplace=True)


data = loadRawData('recipes.csv', 10000)

keepColumns = ['Name',
               #'CookTime', 'PrepTime', 'TotalTime', 
               'RecipeCategory', 'RecipeIngredientQuantities', 'RecipeIngredientParts',
               'RecipeServings', 'RecipeInstructions']
reducedData = selectColumns(data, keepColumns)

removeNullValues(reducedData)


st.dataframe(reducedData)








