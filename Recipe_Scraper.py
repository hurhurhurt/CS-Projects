import requests
import json
import pandas as pd
from numpy import nan
from os import path
from bs4 import BeautifulSoup
import time

def get_links(link):
    """
    Iterates over link and returns a list of links to every recipe contained in each page

    :param link: this is a link to a directory page containing a list of recipes
    :returns: this returns an array containing every link to each recipe in the page
    """
    recipes = []
    page_number = 1
    while True:
        page = link + str(page_number) + "/"
        newPage = requests.get(page)
        if newPage.status_code == 404:
            break
        soup = BeautifulSoup(newPage.content, 'html.parser')
        for page in soup.findAll("a", {"class": "entry-title-link"}):
            recipes.append(page.get('href'))
        page_number += 1
    return recipes


def parse_recipe(link):
    """
    Gathers relevant information from given recipe and stores in a dictionary

    :param link: a link to a recipe
    :returns: a dictionary containing recipe name, prep time, cook time, total time, ingredients, calories,
              review count, ratings, and category.
    """
    print(link) # should print twice
    if requests.get(link).status_code == 404:
        return
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    data = json.loads(soup.find('script', type='application/ld+json').string)
    recipe = next((g for g in data['@graph'] if g.get('@type', '') == 'Recipe'), None)

    if recipe:
        # we use try/except catch blocks because some recipes are missing several parameters
        try:
            name = recipe['name']
        except KeyError:
            name = link
        try:
            prep_time = recipe['prepTime']
        except KeyError:
            prep_time = nan
        try:
            cook_time = recipe['cookTime']
        except KeyError:
            cook_time = nan
        try:
            total_time = recipe['totalTime']
        except KeyError:
            total_time = nan
        try:
            ingredients = str(recipe['recipeIngredient']).strip("['']")
        except KeyError:
            ingredients = nan
        try:
            calories = recipe['nutrition']['calories']
        except KeyError:
            calories = nan
        try:
            review_count = recipe['aggregateRating']['ratingCount']
        except KeyError:
            review_count = nan
        try:
            average_rating = recipe['aggregateRating']['ratingValue']
        except KeyError:
            average_rating = nan
        try:
            category = str(recipe['recipeCategory']).strip("['']")
        except KeyError:
            category = nan
        # creates a dictionary that will be converted into DataFrame for performance purposes
        dictionary = {'Name': name,
                      'Prep Time': prep_time,
                      'Cook Time': cook_time,
                      'Total Time': total_time,
                      'Ingredients': ingredients,
                      'Calories': calories,
                      'Review Count': review_count,
                      'Average Rating': average_rating,
                      'Category': category,
                      'URL': link}

        time.sleep(0.25) # As the website is not big, it's important to take server strain into consideration
        return dictionary


def export_csv(filename, df):
    """
    Generates a csv file from given dataframe.

    :param filename: the name of the file to be created
    :param df: dataframe containing information to be exported
    """

    if not path.isfile(str(filename) + '.csv'):
        df.to_csv(str(filename) + '.csv', index= False)
    else:
        new_filename = input("CSV file exists, please enter a new name: ")
        export_csv(new_filename, df)


def main():
    links = ('https://thewoksoflife.com/category/recipes/noodles-pasta-recipes/page/',
             'https://thewoksoflife.com/category/recipes/rice-recipes/page/',
             'https://thewoksoflife.com/category/recipes/chicken/page/',
             'https://thewoksoflife.com/category/recipes/beef-recipes/page/',
             'https://thewoksoflife.com/category/recipes/fish-and-seafood/page/',
             'https://thewoksoflife.com/category/recipes/pork/page/',
             'https://thewoksoflife.com/category/recipes/lamb/page/',
             'https://thewoksoflife.com/category/recipes/appetizers-and-snacks/page/',
             'https://thewoksoflife.com/category/recipes/bread-and-pizza/page/',
             'https://thewoksoflife.com/category/recipes/chinese-take-out/page/',
             'https://thewoksoflife.com/category/recipes/dessert/page/',
             'https://thewoksoflife.com/category/recipes/vegetables/page/',
             'https://thewoksoflife.com/category/recipes/tofu/page/',
             'https://thewoksoflife.com/category/recipes/soups-and-stocks/page/',
             'https://thewoksoflife.com/category/recipes/vegetarian/page/',
             'https://thewoksoflife.com/category/recipes/quick-and-easy/page/',)

    dict_list = []
    for link in links:
        print("ENTERING NEW CATEGORY: ", link)
        for recipe in get_links(link):
            temp = parse_recipe(recipe)
            if temp:
                dict_list.append(temp)
    recipe_df = pd.DataFrame(dict_list)
    csv_title = input("Please enter a title for the outputted CSV file: ")
    export_csv(csv_title, recipe_df)


if __name__ == "__main__":
    main()
