import requests
import json
import pandas as pd
import time
from numpy import nan
from os import path
from bs4 import BeautifulSoup


def get_links(link):
    ''' iterates over link and returns a list of links to every recipe contained in each page '''
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
    ''' Parses through a webpage and extracts relevant info, returns a dictionary. '''
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    data = json.loads(soup.select_one('script.yoast-schema-graph.yoast-schema-graph--main').text)
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
        url = link
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

        time.sleep(2) # As the website is not big, it's important to take server strain into consideration
        return dictionary


def export_csv(filename, df):
    ''' Requests user to input a file name for output to csv, and if no conflicting filename, creates csv file '''
    if not path.isfile(str(filename) + '.csv'):
        df.to_csv(str(filename) + '.csv', index= False)
    else:
        new_filename = input("CSV file exists, please enter a new name: ")
        export_csv(new_filename, df)


def main():
    links = ['https://thewoksoflife.com/category/recipes/chicken/page/',
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
             'https://thewoksoflife.com/category/recipes/quick-and-easy/page/',
             'https://thewoksoflife.com/category/recipes/rice-and-noodles-recipes/page/']

    # Creates a dictionary of parsed recipes
    dict_list = [parse_recipe(recipe) for link in links for recipe in get_links(link) if parse_recipe(recipe)]
    recipe_df = pd.DataFrame(dict_list)
    csv_title = input("Please enter a title for the outputted CSV file: ")
    export_csv(csv_title, recipe_df)


if __name__ == "__main__":
    main()
