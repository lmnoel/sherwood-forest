import subprocess
from news_api import *
import os.path

def process_headlines():
    process = subprocess.Popen(['java', '-jar', 'NHTextProcessor.jar'],
    	stdout=subprocess.PIPE)
    rating = process.stdout.read().decode('utf-8').split()

    return rating

def update_input():
    api_key = read_api_key()
    headlines = get_all_descs(api_key)

    write_textfile(headlines, 'input.txt','NHResources')

def write_textfile(text,title,path):    
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + '/'+ title
    file = open(file_name,'w') 
    for row in text:
        if row:
            file.write(row) 
    file.close() 

if __name__ == '__main__':
    update_input()
    rating = process_headlines()