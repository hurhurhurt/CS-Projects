import requests
import json
from bs4 import BeautifulSoup

def get_links(link):
    recipes = []
    accum = 1
    while True:
        page = link + str(accum) + "/"
        newPage = requests.get(page)
        if newPage.status_code == 404:
            break
        soup = BeautifulSoup(newPage.content, 'html.parser')
        for i in soup.findAll("a", {"class":"entry-title-link"}):
            recipes.append(i.get('href'))
        accum +=1
    return recipes

def parse_recipe(link):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    data = json.loads(soup.select_one('script.yoast-schema-graph.yoast-schema-graph--main').text)
    #print(json.dumps(data, indent=4))  # <-- uncomment this to print all data

    recipe = next((g for g in data['@graph'] if g.get('@type', '') == 'Recipe'), None)
    if recipe:
        print('Name          =', recipe['name'])
        print('Prep Time     =', recipe['prepTime'])
        print('Cook Time     =', recipe['cookTime'])
        print('Total time    =', recipe['totalTime'])
        print('Ingredients   =', recipe['recipeIngredient'])
        print('Calories      =', recipe['nutrition']['calories'])
        print('Review Count  =', recipe['aggregateRating']['ratingCount'])
        print('Avg Rating    =', recipe['aggregateRating']['ratingValue'])

def main():
    link = "https://thewoksoflife.com/category/recipes/chicken/page/"
    recipes = get_links(link)
    print(recipes)

if __name__ == "__main__":
    main()