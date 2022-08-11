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


data = loadRawData('recipes-sampled.parquet', 100)

keepColumns = ['Name',
               'CookTime', 'PrepTime', 'TotalTime',
               'RecipeCategory',
               'RecipeIngredientParts',
               'RecipeInstructions']

reducedData = selectColumns(data, keepColumns)

convertTimes(reducedData, columns=['CookTime', 'PrepTime', 'TotalTime'])


removeNullValues(reducedData)

# Display Data



recipeCategories = reducedData['RecipeCategory'].unique().tolist()
selection = st.multiselect('Choose category', recipeCategories)
filteredData = reducedData[reducedData['RecipeCategory'].isin(selection)]

#maxTotalTime = int(filteredData['TotalTime'].max())
# max time range arbitrarily set to 120
totalTimeRange = st.slider('Select a range of Total Cooking Time (minutes)', 0, 120, (25, 75))
filteredData = filteredData[(filteredData['TotalTime'] >= totalTimeRange[0]) & (filteredData['TotalTime'] <= totalTimeRange[1])]

st.dataframe(filteredData)
if len(filteredData) == 0:
    st.write('No recipes found')
else:
    st.write(len(filteredData), " recipes found")

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
plt.ylabel('Number of Recipes')
plt.xticks(rotation=90)
plt.xlabel('Recipe Name')
st.pyplot(figCategories)

# Chart for cooking times

st.write('Distribution of Cooking Times')
figTotalTime = plt.figure(figsize=(12, 4))
plt.hist(reducedData['TotalTime'])
plt.ylabel('Number of Recipes')
plt.xticks(rotation=90)
plt.xlabel('Total Cooking Time (minutes)')
st.pyplot(figTotalTime)

# Chart for ingredients

st.write('Count of Ingredients')
def to_1D(series):
    return pd.Series([x for _list in series for x in _list])

topNumberIngredients = 20

labels = to_1D(reducedData['RecipeIngredientParts']).value_counts().index[:topNumberIngredients]
values = to_1D(reducedData['RecipeIngredientParts']).value_counts().values[:topNumberIngredients]

figIngredients = plt.figure(figsize=(12, 4))
plt.bar(labels, values)
plt.ylabel('Number of Recipes')
plt.xticks(rotation=90)
plt.xlabel('Ingredient')
st.pyplot(figIngredients)