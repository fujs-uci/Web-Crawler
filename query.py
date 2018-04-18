
import os
import json
from pprint import pprint
import re
from collections import Counter, defaultdict
import pickle
import Tkinter
import math

data = {}
index = defaultdict(list)

def get_json_data():
        global data     
        #loads up the info as a dict
        with open('WEBPAGES_CLEAN/bookkeeping.json') as data_file:    
                data = json.load(data_file)

def look_for_url(path):
        global data
        #get the url
        return data[path]


def load_dict():
        global index
        #opens the file and gets the dict
        with open('indexed_words.json') as data_file:
                index = json.load( open('indexed_words.json'))
        print(len(index.items()))
        
def top_results(list_of_words):
        top_results = []
        for query_term in list_of_words:
                query_list = index[query_term]
                single_word_query_idf = math.log10(37497/len(query_list))
                query_list = sorted(index[query_term], key= lambda x: math.log10(x[1]) *single_word_query_idf ,reverse = True)
                for doc in query_list[:10]:
                        temp_doc = doc
                        temp_doc.append(query_term)
                        temp_doc[1] = (math.log10(temp_doc[1]) + 1) * single_word_query_idf
                        top_results.append(temp_doc)
        return top_results


def create_doc_dict(list_of_words):
        doc_dict = defaultdict(list)
        top_list = top_results(list_of_words)
        doc_set = set()
        for doc_id, score, weight, term in top_list:
                doc_dict[doc_id].append([score,weight,term])
        for doc_id, term_attributes in doc_dict.items():
                doc_id_score = 0
                for doc_score, doc_weight, doc_terms in term_attributes:
                        doc_id_score += ( doc_weight * doc_score )
                term_attributes.append(doc_id_score)
        sorted_doc_dict = sorted(doc_dict.items(), key= lambda x: x[1][-1], reverse = True)
        return sorted_doc_dict[:10]
                                                        
def find_query(query):
        global index

        try:
                query_list = create_doc_dict(query.strip().split(" "))
                if len(query_list) == 0:
                        print(query+" was not found")
                else:
                        # printing out only the top 10 options
                        for found in query_list[:10]:
                                print(look_for_url(str(found[0])))
        except Exception as e:
                print("Error: {}".format(e))

# The main loop of the program that prompts user's response
def program_running():
        get_json_data()
        load_dict()
        while(True):
                menu()
                menu_options = input("Enter: ")
                if(menu_options == 2):
                        print("Goodbye.")
                        break
                elif(menu_options == 1):
                        query = raw_input("Please Enter Query:")
                        find_query(query)
                else:
                        print("Enter number.")
                
# a trash atempt at a user guift  
def menu():
        menu_list = ["Welcome to Beta-Search","-"*20, "Select Number","-"*20,"(1) Search","(2) Quit","-"*20]
        for item in menu_list:
                print('{:20s}'.format(item))
        
        
if __name__ == '__main__':
        program_running()
