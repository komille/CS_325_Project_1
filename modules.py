import ollama
from bs4 import BeautifulSoup
import requests
from matplotlib import pyplot as plot
import numpy as nplot
def analyze_rating(inputs,outputfile):
    response_list = []
    for input in inputs:                                            #for loop for sending the prompts to phi3
        response = generate_response(input)
        response_list.append(response +'\n')
    with open(outputfile, "a",encoding = 'utf-8') as output:                 #opens file for the responses
        for response in response_list:
            output.write(response)
    return outputfile

def generate_response(input):
    response_list =str()
    phi3_response = ollama.chat(                                 #runs ollama locally
        model="phi3",
        messages=[
        {
            'role': 'user',
            'content': "Please rate the following comment as Negative, Positive, or Neutral:" + input + ". Please only respond with one word.",
        }],
        stream = True,
        options={
            "num_predict":3,
            "temperature":0
        }
        )
    for responses in phi3_response:
        response_list += (responses['message']['content'])
    return response_list

class rating: 
    positive= 0
    negative= 0
    neutral= 0
    name =""
    blankline=0
    def set_product_name(self,name):
        self.name = name
    def positive_increase(self):
        self.positive = self.positive + 1
    def negative_increase(self):
        self.negative = self.negative + 1
    def neutral_increase(self):
        self.neutral = self.neutral + 1
    def count_rating(self,filename):
        with open(filename,"r",encoding="utf-8 ") as ratingfile:
            ratings = ratingfile.readlines()
        for rating in ratings:
            if "Positive" in rating:
                self.positive_increase()
            elif "Negative" in rating: 
                self.negative_increase()
            elif "Neutral" in rating:
                self.neutral_increase()
            else:
                self.blankline = self.blankline
            
        ratingfile.close()
        return self.negative + self.positive + self.neutral

def get_reviews(url):                                           
    stripped_review=[] 
    count = 1 #string for adding reviews 
    
    URL = url.strip()                                                                   #strips url that is read from the file
    request = requests.get(URL)
    soup = BeautifulSoup(request.content, 'html.parser')                                #makes soup for url that is read from file and the first page of reviews
    
    first_page_reviews = soup.find('div',class_='reviews--details')                     #scrapes the review comments from the first page of the product
    first_page_reviews_2 = first_page_reviews.find_all('p',class_='review--content')
    for review in first_page_reviews_2:
        stripped_review.append(review.get_text()+ "\n")                                     #adds review to string

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
            stripped_review.append(rv.get_text()+ "\n")                                     #adds reviews to string

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
    with open(output_filename, "w", encoding='utf-8') as output:                        #opens files for the reviews
        for review in stripped_review:
            output.write(str(count) + ": " + review)                                         #writes review string to file
            count=count +1
    return stripped_review

def create_graph(analyzed_reviews):
    num_objects = len(analyzed_reviews)

     #generate x-axis positions for each object
    x = nplot.arange(num_objects)  


    width = 0.25  # Adjust width to fit bars nicely

    #initialize lists to store sentiment counts for each object
    neutral_counts = [obj.neutral for obj in analyzed_reviews] 
    positive_counts = [obj.positive for obj in analyzed_reviews]
    negative_counts = [obj.negative for obj in analyzed_reviews]

    #creates the figure and axis for plotting
    fig, ax = plot.subplots(figsize=(10, 6))  

    #plot each product sentiment as a separate set of bars
    negative_bar = ax.bar(x - width, negative_counts, width, label='Negative', color='red') 
    positive_bar = ax.bar(x, positive_counts, width, label='Positive', color='blue')
    neutral_bar = ax.bar(x + width, neutral_counts, width, label='Neutral', color='yellow')

    #set labels, title, and legend
    ax.set_xlabel('Products') 
    ax.set_ylabel('Count')
    ax.set_title('Ratings of Products')
    ax.set_xticks(x)
    ax.set_xticklabels([obj.name for obj in analyzed_reviews])
    ax.legend()

    #add value labels on top of bars
    def add_labels(bars):   
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),  
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom')

    #add labels for each set of bars
    add_labels(negative_bar) 
    add_labels(positive_bar)
    add_labels(neutral_bar)

    
    plot.tight_layout() #adjust layout to prevent clipping of labels
    plot.show()  #show the plot
    return fig, ax
