from operator import ge
from random import randint, randrange
from tokenize import Number
from xmlrpc.client import FastMarshaller
import enchant

d = enchant.Dict("en_US")

#TO DO:
#add a third category for letters that are correct in one spot and incorrect in another spot
#without the program thinking there are coonfirmed two instancees of the letter


possible_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#insert black letters

wrong_letters = ['s', 'r',  'e', 'o','g', 'u', 'v', 'm', 'p']

#insert letters as list
#positive- have the right spot
#negative- wrong spot but right letteer
#NOTE this can acceept momre than one letter..i
my_letters = {
    'h': [2],
    'a': [3],
    'c': [-1]

}

def get_random_num(low_num, high_num):
    return randint(low_num, high_num)

def get_random_valid_letter():
    valid_letters = list(set(possible_letters) - set(wrong_letters))
    return valid_letters[get_random_num(low_num=0, high_num=len(valid_letters) - 1)]

def get_valid_index(char, invalid):

    invalid.sort()
    found = False
    counter = 0
    while not found:
        counter += 1
        new_index = get_random_num(low_num=0, high_num=4)
        if new_index not in invalid and my_word[new_index] is None:
            found = True
            return new_index

def know_all_locations_of_char(char_to_check, indices):
    #if there was only one instance of the character
    if len(indices) == 1:
        if indices[0] > 0:
            return True
        else:
            return False
    elif len(indices) > 1:
        known_location = True
        for idx in indices:
            if idx < 0:
                known_location = False
        return known_location

def insert_char(char, idx):
    if my_word[idx] == None:
        my_word[idx] = char

def insert_correct_characters():

    for char,indices in my_letters.items():
        #insert the right characters at the right place
        if know_all_locations_of_char(char, indices):
            for idx in indices:
                insert_char(char, idx -1)

def insert_chars_in_wrong_spot():
    #if the characteer is in the word but in the wrong place 
    #this can handle if theere is more than one instance of a char and 
    #we know one of them
    wrong_indices = []
    for char, indices in my_letters.items():
        if not know_all_locations_of_char(char, indices):
            for idx in indices:
                if idx <0:
                    wrong_indices.append((idx * -1) -1 )
                #if one of the instances is correct insert it
                else:
                    insert_char(char, idx)
            #insert a character at a vaalid index
            valid_index = get_valid_index(char, wrong_indices)
            insert_char(char, valid_index)


found_word = False
num_tries = 1
while not found_word:
    my_word = [None, None, None, None, None]

    insert_correct_characters()
    insert_chars_in_wrong_spot()
    #insert raandom characters
    for index, char in enumerate(my_word):
        if char is None:
            my_word[index] = get_random_valid_letter()
        else:
            continue
           
    new_string = "".join([str(item) for item in my_word])
    if d.check(new_string):
        print("Made a new word! Try guessing %s" % new_string)
        found_word = True
    else:
        print("%s is not a word, num tries: %s" % (new_string, num_tries))
        num_tries += 1
        
        
