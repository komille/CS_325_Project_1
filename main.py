from modules import rating 
from modules import analyze_rating
from modules import get_reviews
from modules import create_graph
from matplotlib import pyplot as plot
count = 5
ratings = []
with open("URLS.txt", "r") as inputfile:                                            #opens file containing the URLS
    URLS = inputfile.readlines() 
for URL in URLS: 
    product_filename = "Amazon_Echo_Dot_"+ str(count) +"_Reviews.txt" 
    get_reviews(URL,product_filename) 
    analyzed_review_file = "Analyzed_" + product_filename           
    analyze_rating(product_filename,analyzed_review_file)

    next_rating = rating()
    next_rating.set_product_name("Amazon Echo Dot "+ str(count))
    next_rating.count_rating(analyzed_review_file)
    ratings.append(next_rating)
    count = count - 1

create_graph(ratings)