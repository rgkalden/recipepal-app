import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Functions

from functions import *

# Title and How To

st.set_page_config(page_title="RecipePal", page_icon="🍲", layout="wide")


st.title("RecipePal 🍲")

with st.expander("How to use this app"):
     st.write("""
         RecipePal is a recipe search tool. You can filter the recipe database by the category, total cooking times, 
         and by ingredient. The resulting recipe information is displayed below, where you
         can also find the instructions. 

         Hints:
         - You can pick multiple categories. Pick a main course, vegetable, and desert to plan a whole meal!
         - In a hurry? Try using the filters for total cooking time. You can choose the minimum and maximum time simultaneously.
         - You can also pick multiple ingredients. Use the "and" method to find recipes containing all ingredients. 
            Use the "or" method to find all recipes that have at least one of the ingredients you picked.
         - It is possible to sort the recipe data by clicking the column headers (sort ascending, descending, alphabetical)
         - It is possible that no recipes matching your search exist. Don't give up, try again!
         - If you really can't decide what to cook, then you can consult the 📊 Analytics page to see what kinds
            of recipes, cooking times, and ingredients exist in the database, and then go back and search.
     """)

# Load and Process data


data = loadRawData('recipes-sampled.parquet', nrows=200)

keepColumns = ['Name',
               'CookTime', 'PrepTime', 'TotalTime',
               'RecipeCategory',
               'RecipeIngredientParts',
               'RecipeInstructions']

reducedData = selectColumns(data, keepColumns)

convertTimes(reducedData, columns=['CookTime', 'PrepTime', 'TotalTime'])

removeNullValues(reducedData)

reducedData = reducedData[reducedData['TotalTime'] <= 200]

# Filters in Sidebar

filteredData = reducedData.copy()

filterOnCategory = st.sidebar.checkbox('Filter by Category')
if filterOnCategory:
    recipeCategories = reducedData['RecipeCategory'].unique().tolist()
    selection = st.sidebar.multiselect('Choose category', recipeCategories)
    filteredData = reducedData[reducedData['RecipeCategory'].isin(selection)]


filterOnTime = st.sidebar.checkbox('Filter by Total Cooking Time')
if filterOnTime:    
    maxCookingTime = int(reducedData['TotalTime'].max())
    minTime = st.sidebar.number_input('Min (minutes)', min_value=0, max_value=maxCookingTime,value=0)
    maxTime = st.sidebar.number_input('Max (minutes)', min_value=0, max_value=maxCookingTime, value=120)
    filteredData = filteredData[(filteredData['TotalTime'] >= minTime) & (filteredData['TotalTime'] <= maxTime)]


filterOnIngredient = st.sidebar.checkbox('Filter by Ingredient(s)')
if filterOnIngredient:
    ingredientList = to_1D(reducedData['RecipeIngredientParts']).value_counts().index.to_list()
    ingredient = st.sidebar.multiselect('Choose ingredients', ingredientList)
    searchMethod = st.sidebar.radio('Search Method', ('and', 'or'), index=0)
    foundIndex = searchItem(filteredData, column='RecipeIngredientParts', target=ingredient, mode=searchMethod)
    if ingredient != '':
        filteredData = filteredData.iloc[foundIndex]


# Display Data


if filterOnCategory or filterOnTime or filterOnIngredient:
    st.dataframe(filteredData, height=220)
else:
    st.dataframe(reducedData, height=220)


# Metrics

numRecipes = len(filteredData)

topNumberIngredients = 10
labels = to_1D(filteredData['RecipeIngredientParts']).value_counts().index.to_list()[:topNumberIngredients]
ingredientMetric = ', '.join(labels)

if numRecipes == 0:
    cookingTimeAvg = 'N/A'
    timeMetricString = 'N/A'
    ingredientMetric = 'N/A'
elif numRecipes == 1:
    cookingTimeAvg = int(filteredData['TotalTime'])
    cookingTimeStd = int(filteredData['TotalTime'])
    timeMetricString = str(cookingTimeAvg) + " min"
else:
    cookingTimeAvg = int(filteredData['TotalTime'].mean())
    cookingTimeStd = int(filteredData['TotalTime'].std())
    timeMetricString = str(cookingTimeAvg) + " ± " + str(cookingTimeStd) + " min"

col1, col2 = st.columns(2)
col1.metric("Number of Recipes", numRecipes, help='Number of recipes currently shown')
col2.metric("Total Cooking Time", timeMetricString, help='Avg ± Std Dev of Total Cooking Times currently shown')

st.write('Common Ingredients')
st.subheader(ingredientMetric)
