# RecipePal 🍲

Welcome to the repository for the RecipePal web app! The app can be viewed at:

[https://rgkalden-recipepal-app--home-rcryl3.streamlitapp.com/](https://rgkalden-recipepal-app--home-rcryl3.streamlitapp.com/)

## Introduction

RecipePal is a web app that is designed to be a recipe database search tool. The app allows for the recipe database to be filtered based on category, cooking time, and ingredients. The app also displays analytics on the database itself to provide insight into what recipes are available, in order to help with a recipe search.

## App Structure

The app is built with Streamlit, and consists of the following files:

* `🏠_Home.py`
* `pages\2_📊_Analytics.py`
* `functions.py`
* `recipes-sampled.parquet`

The app contains two pages, so is broken up with the `pages` folder as required by Streamlit. `functions.py` contains functions used throughout the app, saved in one common file. `recipes-sampled.parquet` is the dataset for the app, which has been randomly sampled from a much larger dataset, using `preprocess-parquet.ipynb`. The original dataset (`recipes.parquet`) is omitted from this repository due to file size constraints, but can be found on Kaggle [here.](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews)

The notebook `explore.ipynb` contains Python code to explore the dataset and experiment with features before incorporating them into the actual app scripts.

## Run the App Locally

With Streamlit installed, a local server can be started to run the app with the following terminal command:

```
streamlit run 🏠_Home.py
```