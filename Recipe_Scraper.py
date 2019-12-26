import requests
import json
import pandas as pd
from bs4 import BeautifulSoup


def get_links(link):
    ''' iterates over link and returns a list of links to every recipe contained in each page '''
    recipes = []
    accum = 1
    while True:
        page = link + str(accum) + "/"
        newPage = requests.get(page)
        if newPage.status_code == 404:
            break
        soup = BeautifulSoup(newPage.content, 'html.parser')
        for page in soup.findAll("a", {"class": "entry-title-link"}):
            recipes.append(page.get('href'))
        accum += 1
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
            prep_time = "NA"
        try:
            cook_time = recipe['cookTime']
        except KeyError:
            cook_time = "NA"
        try:
            total_time = recipe['totalTime']
        except KeyError:
            total_time = "NA"
        try:
            ingredients = recipe['recipeIngredient']
        except KeyError:
            ingredients = "NA"
        try:
            calories = recipe['nutrition']['calories']
        except KeyError:
            calories = "NA"
        try:
            review_count = recipe['aggregateRating']['ratingCount']
        except KeyError:
            review_count = "NA"
        try:
            average_rating = recipe['aggregateRating']['ratingValue']
        except KeyError:
            average_rating = "NA"
        # creates a dictionary that will be converted into DataFrame for performance purposes
        dictionary = {'Name': name, 'Prep Time': prep_time, 'Cook Time': cook_time, 'Total Time': total_time,
                      'Ingredients': ingredients, 'Calories': calories, 'Review Count': review_count,
                      'Average Rating': average_rating}
        return dictionary

def main():
    dict_list = []
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
    for link in links:
        recipes = get_links(link)
        for recipe in recipes:
            dictionary = parse_recipe(recipe)
            if dictionary:
                dict_list.append(dictionary)
    dict_list = pd.DataFrame(dict_list)
    dict_list.to_csv("Recipes.csv")


if __name__ == "__main__":
    main()
