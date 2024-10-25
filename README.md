## Package Downloads
    1.BeautifulSoup (used to scrap html from websites being scraped)
    2.requests (used to send http requests to the website that is being scraped)
## File Downloads
    1.Download requirements.yaml file
    2.Download URLS.txt and webscraper.py
## Running the Code
    1. Have conda installed 
    2. Run command conda env create -f requirements.yaml to create a conda environment with the requirements 
    3. Run webscraper.py inside the environment in vs code
    4. An output file Amazon_Echo_Dot_#_Reviews.txt will be created for each input url in URLS.txt
    5. The output files will contain reviews scraped from the websites from the urls in URLS.txt
## What the Program Does
    This program takes Ebay URLS as input and returns an output file for each url that contains the reviews for the product on Ebay