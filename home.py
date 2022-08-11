import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("RecipePal 🍲")

with st.expander("How to use this app"):
     st.write("""
         How to
     """)

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


def stringToList(string):
    cleanedString = string.replace('[', '').replace(']', '').replace('\'', '')
    list = cleanedString.split(' ')
    return list

def cleanStringSeries(dataframe, columns):
    for column in columns:
        dataframe[column] = dataframe[column].apply(stringToList)


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

cleanStringSeries(reducedData, columns=['RecipeIngredientParts', 'RecipeInstructions'])


removeNullValues(reducedData)

# Display Data

#st.subheader('Recipe Database')
#st.dataframe(reducedData)

maxTotalTime = int(reducedData['TotalTime'].max())
# max time range arbitrarily set to 120
totalTimeRange = st.slider('Select a range of Total Cooking Time (minutes)', 0, 120, (25, 75))
filteredData = reducedData[(reducedData['TotalTime'] >= totalTimeRange[0]) & (reducedData['TotalTime'] <= totalTimeRange[1])]

recipeCategories = filteredData['RecipeCategory'].unique().tolist()
selection = st.multiselect('Choose category', recipeCategories)
filteredData = filteredData[filteredData['RecipeCategory'].isin(selection)]

st.dataframe(filteredData)

# Can't decide what to eat? Visualize recipe database

st.subheader('Not sure what you want to cook? 😕')
st.write('Visualization of your recipe database')

# Chart for recipe categories

topNumberCategories = st.slider('Number of categories to display?', 0, 20, 10)
st.write('Top ', topNumberCategories, 'categories are displayed')
topCategories = reducedData['RecipeCategory'].value_counts().index.to_list()[:topNumberCategories]
topCategoriesDataframe = reducedData[reducedData['RecipeCategory'].isin(
    topCategories)]

figCategories = plt.figure(figsize=(12, 4))
plt.hist(topCategoriesDataframe['RecipeCategory'])
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.xlabel('Recipe Name')
st.pyplot(figCategories)

# Chart for cooking times

st.write('Distribution of Cooking Times')
figTotalTime = plt.figure(figsize=(12, 4))
plt.hist(reducedData['TotalTime'])
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.xlabel('Total Cooking Time (minutes)')
st.pyplot(figTotalTime)
