import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Functions

from functions import *

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

# Title
st.title('Analytics')

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