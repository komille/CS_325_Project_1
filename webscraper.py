from bs4 import BeautifulSoup
import requests
count = 5

with open("URLS.txt", "r") as inputfile:                                            #opens file containing the URLS
    URLS = inputfile.readlines() 


for URL in URLS:                                                                    #loops through each url to scrape the data
    stripped_review=''                                                              #string for adding reviews 
    
    URL = URL.strip()                                                                   #strips url that is read from the file
    request = requests.get(URL)
    soup = BeautifulSoup(request.content, 'html.parser')                                #makes soup for url that is read from file and the first page of reviews
    
    first_page_reviews = soup.find('div',class_='reviews--details')                     #scrapes the review comments from the first page of the product
    first_page_reviews_2 = first_page_reviews.find_all('p',class_='review--content')
    for review in first_page_reviews_2:
        stripped_review +=review.get_text()+ "\n\n"                                     #adds review to string

    next_url = soup.find('div',class_ ='reviews--head')                                 #scrapes the url for the first next review page    
    next_url_2 = next_url.find_all('a')
    stripped_url = ''
    for url in next_url_2:
        stripped_url += url.get('href')                                                 #gets the url from the next page button
    next_page= stripped_url.strip()                                                     #strips the url for the next review page
    
    eop = bool
    while(eop != True):                                                                 #loops through following review pages
        request = requests.get(next_page)                                               
        soup = BeautifulSoup(request.content, 'html.parser')                            #makes soup for following review pages

        follow_review = soup.find('div', class_='reviews')                                                 #scrapes review comments for the following review pages
        all_reviews= follow_review.find_all('p', class_ = 'review-item-content rvw-wrap-spaces')
        for rv in all_reviews:
            stripped_review+= rv.get_text()+ "\n\n"                                     #adds reviews to string

        next_url_while= soup.find_all('a','spf-link')                                   #scrapes the following review page urls
        new_url =''
        rel=''
        for url in next_url_while:                                                    
            rel= url.get('rel')
            if(rel==["next"]):
                new_url+= url.get('href')+"\n\n"                                      #gets url from scraped data
        next_page = new_url.strip()                                                   #strips the url for the following the review pages
        eof_rel=''
        end_of_pages= soup.find_all('a','spf-link')
        for eof in end_of_pages:                                                                #finds the end of review pages 
            rel= url.get('class')
            if(rel==["disabled" , "spf-link"]):
                eop =True
    with open("Amazon_Echo_Dot_"+ str(count)+"_Reviews.txt", "w", encoding='utf-8') as output:                        #opens files for the reviews
        output.write(stripped_review)                                                #writes review string to file
        count = count - 1

inputfile.close()

