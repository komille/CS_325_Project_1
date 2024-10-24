from bs4 import BeautifulSoup
import requests
count = 5

with open("URLS.txt", "r") as inputfile:                                            #opens file containing the URLS
    URLS = inputfile.readlines() 


for URL in URLS:
    stripped_review=''
    
    URL = URL.strip()                                                                   #strips url that is read from the file
    request = requests.get(URL)
    soup = BeautifulSoup(request.content, 'html.parser')                                #makes soup for url that is read from file
    
    first_page_reviews = soup.find('div',class_='reviews--details')                     #pulls the reviews from the first page of the product
    first_page_reviews_2 = first_page_reviews.find_all('p',class_='review--content')
    for review in first_page_reviews_2:
        stripped_review +=review.get_text()+ "\n\n"

    next_url = soup.find('div',class_ ='reviews--head')                                 #pulls the url for the first next review page    
    next_url_2 = next_url.find_all('a')
    stripped_url = ''
    for url in next_url_2:
        stripped_url += url.get('href')
    next_page= stripped_url.strip()
    
    eop = bool
    while(eop != True):
        request = requests.get(next_page)                                                  #pulls the url for the following next review pages
        soup = BeautifulSoup(request.content, 'html.parser')

        follow_review = soup.find('div', class_='reviews')                                                 #pull comments for the following review pages
        all_reviews= follow_review.find_all('p', class_ = 'review-item-content rvw-wrap-spaces')
        for rv in all_reviews:
            stripped_review+= rv.get_text()+ "\n\n"

        next_url_while= soup.find_all('a','spf-link')
        new_url =''
        rel=''
        for url in next_url_while:
            rel= url.get('rel')
            if(rel==["next"]):
                new_url+= url.get('href')+"\n\n"
        next_page = new_url.strip()
        eof_rel=''
        end_of_pages= soup.find_all('a','spf-link')
        for eof in end_of_pages:
            rel= url.get('class')
            if(rel==["disabled" , "spf-link"]):
                eop =True
    with open("Amazon Echo Dot "+ str(count)+" Reviews.txt", "w", encoding='utf-8') as output:                        #opens files for the reviews
        output.write(stripped_review)
        count = count - 1

inputfile.close()
