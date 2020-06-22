from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from fractions import Fraction
from re_vulgar_fractions import check_vulgar
from string_to_object import clean_string, get_multiple_items
import sys
import json


def make_recipe_list(url):
    #Normal: https://www.shelikesfood.com/crispy-baked-black-bean-sweet-potato-tacos/
    # url = 'https://30daysofgreekfood.com/greek-white-bean-soup-fasolada-lemon-tomato/'
    # print(url)
    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')



    lists = soup.select('body ul')

    data = {}

    # class recipe_item(): #Not used rn
        # def __init__(self, item_str):
        #     #take out vulgar fractions
        #     item_str = check_vulgar(item_str)
            
        #     self.amount = get_amount(item_str)
        #     self.get_measurement(item_str)
        #     self.name = get_name(item_str)

        #     pass
        
        # def get_amount(self, item_str):
        #     #split by number, and measurement
            
        #     pass

        # def get_name(self, item_str):
        #     pass
        


    recipe_items_list = []
    for li in lists: #look through all lists on the webpage
        
        if len(li.contents) < 1: #Skip empty lists
            break

        i = 0
        while i < len(li.contents) and (isinstance(li.contents[i], Tag) is False): #This gets rid of errors where non li elements are part of the list like ('\n)
            i += 1

        first_item = li.contents[i].text

        #Counters to check what fraction of list items start with a number
        num_items = 0
        items_w_nums = 0

        if len(first_item) > 0: #make sure there is text present in the list

            #loop through the list
            for item in li.contents:
                # item.text.strip()
                if isinstance(item, Tag): #This gets rid of errors where non li elements are part of the list like ('\n)
                    if item.text.strip()[0].isdigit(): #strip removes any leading and trailing whitespace
                        items_w_nums += 1
                    num_items += 1
                

            if items_w_nums / num_items > 0.5:
                #append recipe_items to 
                for item in li.contents:
                    if isinstance(item, Tag): #This gets rid of errors where non li elements are part of the list like ('\n)
                        # new_item = recipe_item(item.text)
                        #clean text
                        #split if there's an and
                        cleaned_item = clean_string(item.text)
                        
                        for many_item in get_multiple_items(cleaned_item):
                            recipe_items_list.append(many_item)

    # for item in recipe_items_list:   
        
    #     print(item)
    data['items'] = recipe_items_list
    json_data = json.dumps(data)
    print(json_data) #this sends it to stdout so it can be used by node
    return recipe_items_list

# print("== argv1")
# print(sys.argv[1])

make_recipe_list(sys.argv[1])

# print(recipe[0])
# 'https://diethood.com/roasted-garlic-parmesan-carrots/'