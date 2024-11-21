import pytest
from modules import rating
from modules import analyze_rating
from modules import create_graph

#uses test data to test count_rating method
def test_count_rating():
    test_rating = rating()
    assert test_rating.count_rating("test_data\count_rating_test_data.txt") == 6 
    assert test_rating.neutral == 2
    assert test_rating.positive == 1
    assert test_rating.negative == 3

#tests analyze rating function using test data
def test_analyze_rating():
    test_output = []
    analyze_rating("test_data\Analyze_rating_test_data","out.txt")
    with open("out.txt", "r",encoding ='utf-8') as inputfile:
        inputs = inputfile.readlines()
        for input in inputs:
            test_output.append(input)
    assert test_output == ['Positive\n','Positive\n','Negative\n','Neutral\n']   

#tests the create graph function with test data
def test_graph():
    class TestRating:
        def __init__(self, name, positive, negative, neutral):
            self.name = name
            self.positive = positive
            self.negative = negative
            self.neutral = neutral
    mock_ratings = [
        TestRating(name="Product A", positive=10, negative=5, neutral=3),
        TestRating(name="Product B", positive=8, negative=6, neutral=6),
    ]

    fig, ax = create_graph(mock_ratings)

    #tests values of title,x-axis label, and y-axis label
    assert ax.get_title() == 'Ratings of Products' 
    assert ax.get_xlabel() == 'Products'
    assert ax.get_ylabel() == 'Count'
    
    #tests individual labels for each product
    expected_labels = ["Product A", "Product B"]
    actual_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    assert actual_labels == expected_labels

    
#tests assignment in rating class
def test_rating_assign():
    test_rating = rating()
    test_rating.set_product_name("test")
    test_rating.neutral_increase()
    test_rating.positive_increase()
    test_rating.negative_increase()
    assert test_rating.name == "test"
    assert test_rating.positive == 1
    assert test_rating.negative == 1
    assert test_rating.neutral == 1






    


