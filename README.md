# Recipe Recommender System w/ Data Analysis, NLP, and Full-Stack Web App (in progress)

**About:**
This is a project to celebrate the diversity of Asian Food through data visualization of thousands of Asian recipes. The program will also include a recommender system in the future, where based on a user's available ingredients, will suggest a highly rated recipe. All data is scraped from thewoksoflife.com, and I greatly thank them for allowing me the opportunity to conduct this project.

**Installation:**
To scrape recipes, simply installing and running the Recipe_Scraper.py file will generate an uncleaned csv file (the terminal will ask you to name this csv file). If you would prefer to simply see the visualization, all relevant graphs will be available inside the repo; otherwise, you can view them in the .ipynb file.

**Future Work**
Currently, I am working on developing the NLP model to, based on similar ingredients, recommend the recipes that have similar materials needed and match the user's criteria. After this, I plan on developing a full-stack web application that users can utilize to get recommendations on what they should cook! In the far future, I hope to brush up on my Data Engineering capabilities and create a robust ETL pipeline that can allows users to dynamically rate recipes themselves, and use this to build a collaborative filtering-based recommendation engine that is hopefully more accurate than the static one I have built.

Furthermore, the data cleaning I performed was not very robust, and involved a good bit of manual work to properly parse each recipe and ensure everything was in the right place. For example, given the sentence "1 tablespoon lemon juice", it is extremely difficult, if not impossible, to develop a regular expression capable of parsing the unit quantity, the unit measure, and the ingredient, for all cases (for example, 1 tablespoon lemon juice vs five pinches of salt). In the future, I plan on developing, based on a similar scraper created by the New York Times, a linear-chain conditional random field (CRF) trained on tens of thousands of recipes from websites like Allrecipes, Food Network, etc that will be able to properly differentiate ingredients. 

**Credits:**
thewoksoflife.com
