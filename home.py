import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


def searchItem(dataframe, column, target):
    series = dataframe[column].to_list()

    foundIndex = []
    for i in range(0, len(series)):
        for item in series[i]:
            if item == target:
                foundIndex.append(i)

    return foundIndex


def to_1D(series):
    return pd.Series([x for _list in series for x in _list])


# Title and How To


st.title("RecipePal 🍲")

with st.expander("How to use this app"):
     st.write("""
         RecipePal is a recipe search tool. You can search by the recipe category, range of cooking times, 
         and also by ingredient. The resulting recipe information is displayed below, where you
         can also find the instructions. 
         
         It is possible that no recipes matching your search exist. Don't give up, try again!

         If you really can't decide what to cook, then you can consult the charts below to see what kinds
         of recipes, cooking times, and ingredients exist, then go back and search.
     """)

# Load and Process data


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

filterOnCategory = st.checkbox('Filter on Category')

if filterOnCategory:
    recipeCategories = reducedData['RecipeCategory'].unique().tolist()
    selection = st.multiselect('Choose category', recipeCategories)
    filteredData = reducedData[reducedData['RecipeCategory'].isin(selection)]


filterOnTime = st.checkbox('Filter on cooking time')

if filterOnTime:    
    maxCookingTime = int(reducedData['TotalTime'].max())
    totalTimeRange = st.slider('Select a range of Total Cooking Time (minutes)', 0, maxCookingTime, (0, 120))
    filteredData = filteredData[(filteredData['TotalTime'] >= totalTimeRange[0]) & (filteredData['TotalTime'] <= totalTimeRange[1])]

filterOnIngredient = st.checkbox('Filter by Ingredient')

if filterOnIngredient:
    ingredient = st.text_input('Ingredient Name', '')

    foundIndex = searchItem(filteredData, column='RecipeIngredientParts', target=ingredient)
    if ingredient != '':
        filteredData = filteredData.iloc[foundIndex]

if filterOnCategory or filterOnTime or filterOnIngredient:
    st.dataframe(filteredData)

    if len(filteredData) == 0:
        st.write('No recipes found')
    else:
        st.write(len(filteredData), " recipes found")


# Visualize recipe database


st.subheader('Not sure what you want to cook? 😕')
st.write('Visualization of your recipe database')


# Chart for recipe categories


topNumberCategories = st.slider('Number of categories to display?', 0, 20, 10)
st.write('Top ', topNumberCategories, 'categories are displayed')
topCategories = reducedData['RecipeCategory'].value_counts().index.to_list()[:topNumberCategories]
topCategoriesDataframe = reducedData[reducedData['RecipeCategory'].isin(topCategories)]

figCategories = plt.figure(figsize=(12, 4))
plt.hist(topCategoriesDataframe['RecipeCategory'])
plt.ylabel('Number of Recipes')
plt.xticks(rotation=90)
plt.xlabel('Recipe Name')
st.pyplot(figCategories)


# Chart for cooking times


st.write('Distribution of Cooking Times')
figTotalTime = plt.figure(figsize=(12, 4))
plt.hist(topCategoriesDataframe['TotalTime'])
plt.ylabel('Number of Recipes')
plt.xticks(rotation=90)
plt.xlabel('Total Cooking Time (minutes)')
st.pyplot(figTotalTime)


# Chart for ingredients


st.write('Distribution of Ingredients')

topNumberIngredients = 20
labels = to_1D(topCategoriesDataframe['RecipeIngredientParts']).value_counts().index[:topNumberIngredients]
values = to_1D(topCategoriesDataframe['RecipeIngredientParts']).value_counts().values[:topNumberIngredients]

figIngredients = plt.figure(figsize=(12, 4))
plt.bar(labels, values)
plt.ylabel('Number of Recipes')
plt.xticks(rotation=90)
plt.xlabel('Ingredient')
st.pyplot(figIngredients)