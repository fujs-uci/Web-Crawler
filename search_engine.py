import os
import json

class tokenizer:
        def __init__(self):
                self.folder_name = input("Create Inverted index from folder.\n-->")
                self.getDirectories()
                print(self.path_list)

        def getDirectories(self):
                self.path_list = []
                for dir in os.listdir(self.folder_name):
                        path = "{}/{}".format(self.folder_name,dir)
                        if(os.path.isdir(path)):
                                self.path_list.append(path)
                
                
class search_engine:
        def __init__(self):
                program_running = True
                while(program_running):
                        query = input("Query: ")
                        if(query == "quit"):
                                program_running = False
                                

if __name__ == '__main__':
        tokenizer()
        search_engine()
        print("Goodbye")
