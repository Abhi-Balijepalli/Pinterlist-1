import nltk
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from re_vulgar_fractions import check_vulgar
import re

measurement_types = {
    'gallon': True, 'cup': True, 'drop': True, 'quart': True, 'liter': True, 'milliliter': True, 'pint': True, 'l': True, 
    'ml': True, 'ltr': True, 'ounce': True, 'tablespoon': True, 'teaspoon': True, 'gram': True, 'kilogram': True, 'dash': True, 'pinch': True,
    'pound': True, 'stick': True, 'oz': True, 'tbsp': True, 'tsp': True, 'g': True, 'kg':True, 'lb': True, 'handful': True
}

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#goal is to get the numbers and nouns then turn those into 

#clean the string. Get rid of vulgar fractions, make all lowercase, strip extra words.
def clean_string(input_string):

    ### delete with numbers that have weights associated with them (we only want quantities)
    weight_measurement_units = {
        'ounce': True, 'gram': True, 'kilogram': True, 'pound': True, 'oz': True, 'g': True, 'kg':True, 'lb': True
    }
   
    
    tokenized_str = input_string.split() #tokenize input_str
    i = 0
    while i < len(tokenized_str):

        pattern = re.compile(r'[a-zA-Z]+') #make sure the units are clean (ex. 14oz. -> oz)
        curr_str = re.search(pattern,tokenized_str[i])
        
        try:
            #remove the first number to the left of a weight measurement unit
            if curr_str[0] in weight_measurement_units: 
                del_str = tokenized_str[i]
                del tokenized_str[i]
                i += 1
                if hasNumbers(del_str) is False:
                    for j in reversed(range(0, (i-1))): #remove the digit to the left of the measurement unit
                        # float_str = int(tokenized_str[j])
                        if hasNumbers(tokenized_str[j]):
                            del tokenized_str[j]
                            break

                break #only do once
        
        except:
            pass
        
        i += 1
    input_string = ' '.join(tokenized_str)


    ##get rid of info in parenthesis or after a comma
    pattern_list = [re.compile(r'\((.*?)\)'), re.compile(r'[,].*'), re.compile(r'\sto\s.*')] #finds all text in a parenthesis and all text after a comma
    
    for pattern in pattern_list: #removes all matches 
        input_string = re.sub(pattern, '', input_string)


    ##make all lowercase
    input_string = input_string.lower()
    ##get rid of vulgar fractions
    input_string = check_vulgar(input_string)

    
    #TODO turn written numbers into numeric. ex. one -> 1, twelve -> 12
    
   
    


    return input_string

def get_multiple_items(cleaned_string):
    #Input: string cleaned by clean_string function
    #Output: list of items. (list of one of there weren't multiple recipe items in the string)
    and_variations = {
        'And':True, 'and':True, '&': True, '\+': True
    }

    for var in and_variations:
        if var in cleaned_string:
            items = re.split(rf"\s{var}\s", cleaned_string)
            if len(items) > 1: #make sure a split happened. (could've found 'and' in a word like 'handful')
            # items = cleaned_string.split(var)
                return items
        

    return [cleaned_string]


# input_str = '2 cans lentils 14 oz. (or 3 cups cooked), drained and rinsed'

# # woe = clean_string(input_str)
# woohoo = clean_string('salt & fresh cracked pepper, to taste')

# yay = get_multiple_items(woohoo)
# yayy = 0

def get_quantity(cleaned_string):
    

    pass


def is_food(word):

    syns = wn.synsets(str(word), pos = wn.NOUN)

    for syn in syns:
        if 'food' in syn.lexname():
            return 1
    return 0

def is_measurement_unit(word):

    if word in measurement_types:
        print(f'{word} is a measurement type!')
    else:
        print(f'{word} is not a measurement type!')


def process_tokenized(tokenized):
    quantity_arr = []
    noun_arr = [] #stores multiple nouns if they're present ex: dijon mustard -> ['dijon', 'mustard']
    measure_unit = '' 
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            pos = tagged[0][1] #part of speech
            curr_word = tagged[0][0]

            if pos == 'CD':
                quantity_arr.append(float(curr_word))

            if pos == 'NN':
                if is_food(curr_word):
                    noun_arr.append(curr_word)
                if is_quantity(curr_word):
                    measure_unit = curr_word
            print(tagged)

            quantity = sum(quantity_arr)
            food_item = ''.join(noun_arr)



    except Exception as e:
        print(str(e))



def make_recipe_item(input_string):
    #To make more efficient take input as string from user_view_recipe_item so it only has to be cleaned once

    #Input: text from an ingredient in a pin
    #Output: a recipe item containing the quantity and food item name

    input_string = clean_string(input_string)

    #Re-look into this code and the process_tokenized functions
    # tokenized = word_tokenize(input_string)
    # process_tokenized(tokenized)


    pass


make_recipe_item('3 ½ cup Dijon mustard')


