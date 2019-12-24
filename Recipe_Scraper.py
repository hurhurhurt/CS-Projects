import requests
from bs4 import BeautifulSoup


def parse(link):
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
            print(i.get('href'))
        accum +=1

def main():
    link = "https://thewoksoflife.com/category/recipes/chicken/page/"
    recipes = parse(link)


if __name__ == "__main__":
    main()