import requests
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
            #print(i.get('href'))
        accum +=1
    return recipes

def parse_recipe(link):
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        for i in soup.findAll("script", {"class": "yoast-schema-graph yoast-schema-graph--main"}):
            for j in i.descendants:
                print(j.name)
    except:
        pass

def main():
    parse_recipe("https://thewoksoflife.com/cantonese-chicken-feet-soup/")
    #link = "https://thewoksoflife.com/category/recipes/chicken/page/"
    #recipes = get_links(link)
    #print(recipes)


if __name__ == "__main__":
    main()