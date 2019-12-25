import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

# iterates over link and returns a list of links to every recipe contained in each page
def get_links(link):
    recipes = []
    # recipe pages start with a /1/ and increment by 1 for each page, we will use an accumulator to iterate through each page
    accum = 1
    while True: 
        page = link + str(accum) + "/"        
        newPage = requests.get(page)
        if newPage.status_code == 404:
            break
        soup = BeautifulSoup(newPage.content, 'html.parser')
        for i in soup.findAll("a", {"class":"entry-title-link"}):
            recipes.append(i.get('href')) # adds every link found in the current page to the list
        accum +=1
    return recipes

# creates a dataframe of parsed name, ingredients, calories, etc and appends it to existing dataframe
def parse_recipe(link, df):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    data = json.loads(soup.select_one('script.yoast-schema-graph.yoast-schema-graph--main').text)

    recipe = next((g for g in data['@graph'] if g.get('@type', '') == 'Recipe'), None)
    if recipe:
        # we use try/except catch blocks because some recipes are missing several parameters: this prevents the program from stopping during execution
        try:
            name = recipe['name']
        except KeyError:
            name = link
        try:
            prep_time = recipe['prepTime']
        except KeyError:
            prep_time = 0
        try:
            cook_time = recipe['cookTime']
        except KeyError:
            cook_time = 0
        try:
            ingredients = recipe['recipeIngredient']
        except KeyError:
            ingredients = ""
        try:
            calories = recipe['nutrition']['calories']
        except KeyError:
            calories = -1
        try:
            review_count = recipe['aggregateRating']['ratingCount']
        except KeyError:
            review_count = -1
        try:
            average_rating = recipe['aggregateRating']['ratingValue']
        except KeyError:
            average_rating = -1
        data = [[name, prep_time, cook_time, ingredients, calories, review_count, average_rating]]
        temp_df = pd.DataFrame(data, columns=['Name', 'Prep Time', 'Cook Time', 'Ingredients',
                                                     'Calories', 'Review Count', 'Avg Rating'])
        result = pd.concat([df, temp_df], sort=True)
        return result

# creates empty dataframe where recipes will be appended
def create_df():
    df = pd.DataFrame(columns=['Name', 'Prep Time', 'Cook Time', 'Ingredients', 'Calories', 'Review Count', 'Avg Rating'])
    return df


if __name__ == "__main__":
    link = "https://thewoksoflife.com/category/recipes/chicken/page/"
    recipes = get_links(link)
    df = create_df()
    for i in recipes:
        df = parse_recipe(i, df)
    print(df.to_string())
    df.to_csv('plswork.csv')