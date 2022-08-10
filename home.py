import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("RecipePal")

@st.cache()
def loadRawData(filename, nrows):
    return pd.read_parquet(filename)[:nrows]


def selectColumns(dataframe, columns):
    newDataframe = dataframe.copy()
    return newDataframe[columns]

def convertTimes(dataframe, columns):
    for column in columns:
        dataframe[column] = pd.to_timedelta(dataframe[column], errors='coerce') / np.timedelta64(1, 'm')


def removeNullValues(dataframe):
    dataframe.dropna(axis=0, inplace=True)


data = loadRawData('recipes.parquet', 100)

keepColumns = ['Name',
               'CookTime', 'PrepTime', 'TotalTime', 
               'RecipeCategory', 
               #'RecipeIngredientQuantities', 
               'RecipeIngredientParts',
               'RecipeInstructions']

reducedData = selectColumns(data, keepColumns)

convertTimes(reducedData, columns=['CookTime', 'PrepTime', 'TotalTime'])

removeNullValues(reducedData)


st.dataframe(reducedData)


figCategories = plt.figure(figsize=(12, 4))
plt.hist(reducedData['RecipeCategory'], bins=30)
plt.title('Recipe Categories')
plt.ylabel('Count')
plt.xticks(rotation=90)
st.pyplot(figCategories)

figTotalTime = plt.figure(figsize=(12, 4))
plt.hist(reducedData['TotalTime'], bins=30)
plt.title('Cooking Times')
plt.ylabel('Count')
plt.xticks(rotation=90)
st.pyplot(figTotalTime)






