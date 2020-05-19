# Recipe Recommender System w/ Data Analysis, NLP, and Full-Stack Web App (in progress)

**About:**
This is a project to celebrate the diversity of Asian Food through data visualization of thousands of Asian recipes. It includes a web scraper for thewoksoflife.com, an Asian recipe website with some of the most delicious recipes for Asian food on the web. Furthermore, it includes an end-to-end data cleaning, exploratory data analysis, and recommender system model that is dynamic based on user input and will recommend recipes similar to what users enjoy using a cosine similarity NLP algorithm. 

**Installation:**
To scrape recipes, simply installing and running the Recipe_Scraper.py file will generate an uncleaned csv file (the terminal will ask you to name this csv file). If you would prefer to simply see the visualization, all relevant graphs will be available inside the repo; otherwise, you can view them in the .ipynb file. If you would like to see the NLP model, you can view it in "Recipe_Recommender_System.ipynb". 

**Future Work:**
I am actively working on improving the NLP model by adding weights to the type of protein for better accuracy in recipe similarity, as well as allowing users to indicate ingredients they don't have and/or any food allergies.

Furthermore, the data cleaning I performed was not very robust, and involved a good bit of manual work to properly parse each recipe and ensure everything was in the right place. For example, given the sentence "1 tablespoon lemon juice", it is extremely difficult, if not impossible, to develop a regular expression capable of parsing the unit quantity, the unit measure, and the ingredient, for all cases (for example, 1 tablespoon lemon juice vs five pinches of salt). In the future, I plan on developing, based on a similar scraper created by the New York Times, a linear-chain conditional random field (CRF) trained on tens of thousands of recipes from websites like Allrecipes, Food Network, etc that will be able to properly differentiate ingredients.

Lastly, I will develop a full-stack web application once these issues are resolved taking in the recommender system. I will focus on a data engineering aspect here, building an ETL pipeline to allow users to rate the recipes they are given with userID, allowing for better recommendations because collaborative filtering can then be used.

**Credits:**
thewoksoflife.com
