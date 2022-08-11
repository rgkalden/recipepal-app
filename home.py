import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("RecipePal")

# Load and Process data


@st.cache()
def loadRawData(filename, nrows):
    return pd.read_csv(filename)[:nrows]


def selectColumns(dataframe, columns):
    newDataframe = dataframe.copy()
    return newDataframe[columns]


def convertTimes(dataframe, columns):
    for column in columns:
        dataframe[column] = pd.to_timedelta(
            dataframe[column], errors='coerce') / np.timedelta64(1, 'm')


def removeNullValues(dataframe):
    dataframe.dropna(axis=0, inplace=True)


data = loadRawData('recipes.csv', 100)

keepColumns = ['Name',
               'CookTime', 'PrepTime', 'TotalTime',
               'RecipeCategory',
               # 'RecipeIngredientQuantities',
               'RecipeIngredientParts',
               'RecipeInstructions']

reducedData = selectColumns(data, keepColumns)

convertTimes(reducedData, columns=['CookTime', 'PrepTime', 'TotalTime'])

removeNullValues(reducedData)

# Display Data

st.subheader('Recipe Database')
#st.dataframe(reducedData)

maxTotalTime = int(reducedData['TotalTime'].max())
totalTimeRange = st.slider('Select a range of Total Cooking Time (minutes)', 0, 120, (25, 75))
filteredData = reducedData[(reducedData['TotalTime'] >= totalTimeRange[0]) & (reducedData['TotalTime'] <= totalTimeRange[1])]
st.dataframe(filteredData)

# Chart for recipe categories

st.subheader('Most Frequently Cooked Recipe Categories')
topNumberCategories = st.slider('Number of categories to display?', 0, 20, 10)
topCategories = filteredData['RecipeCategory'].value_counts().index.to_list()[:topNumberCategories]
topCategoriesDataframe = reducedData[reducedData['RecipeCategory'].isin(
    topCategories)]

figCategories = plt.figure(figsize=(12, 4))
plt.hist(topCategoriesDataframe['RecipeCategory'])
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.xlabel('Recipe Name')
st.pyplot(figCategories)

# Chart for cooking times

st.subheader('Distribution of Cooking Times')
figTotalTime = plt.figure(figsize=(12, 4))
plt.hist(filteredData['TotalTime'])
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.xlabel('Total Cooking Time (minutes)')
st.pyplot(figTotalTime)
