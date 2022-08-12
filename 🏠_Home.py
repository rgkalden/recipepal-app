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


def displayNumberOfRecipes(dataframe):
    if len(dataframe) == 0:
        st.write('No recipes found')
    else:
        st.write(len(dataframe), " recipes found")


# Title and How To


st.title("RecipePal 🍲")

with st.expander("How to use this app"):
     st.write("""
         RecipePal is a recipe search tool. You can filter the recipe database by the category, total cooking times, 
         and by ingredient. The resulting recipe information is displayed below, where you
         can also find the instructions. 
         
         It is possible that no recipes matching your search exist. Don't give up, try again!

         If you really can't decide what to cook, then you can consult the 📊 Analytics page to see what kinds
         of recipes, cooking times, and ingredients exist in the database, and then go back and search.
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

filterOnCategory = st.sidebar.checkbox('Filter on Category')

filteredData = reducedData.copy()

if filterOnCategory:
    recipeCategories = reducedData['RecipeCategory'].unique().tolist()
    selection = st.sidebar.multiselect('Choose category', recipeCategories)
    filteredData = reducedData[reducedData['RecipeCategory'].isin(selection)]


filterOnTime = st.sidebar.checkbox('Filter on Total Cooking Time')

if filterOnTime:    
    maxCookingTime = int(reducedData['TotalTime'].max())
    minTime = st.sidebar.number_input('Min (minutes)', min_value=0, max_value=maxCookingTime,value=0)
    maxTime = st.sidebar.number_input('Max (minutes)', min_value=0, max_value=maxCookingTime, value=120)
    filteredData = filteredData[(filteredData['TotalTime'] >= minTime) & (filteredData['TotalTime'] <= maxTime)]

filterOnIngredient = st.sidebar.checkbox('Filter by Ingredient')

if filterOnIngredient:
    ingredient = st.sidebar.text_input('Ingredient Name', '')

    foundIndex = searchItem(filteredData, column='RecipeIngredientParts', target=ingredient)
    if ingredient != '':
        filteredData = filteredData.iloc[foundIndex]

if filterOnCategory or filterOnTime or filterOnIngredient:
    st.dataframe(filteredData)
    displayNumberOfRecipes(filteredData)
else:
    st.dataframe(reducedData)
    displayNumberOfRecipes(reducedData)


