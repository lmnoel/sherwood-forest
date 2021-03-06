import requests
import json

SOURCES = ['bloomberg','cnbc', 'financial-times','fortune','reuters','the-wall-street-journal']


def read_api_key():
    file = open('news_api_key.txt','r')
    rv = file.read()[:-1]
    return rv

def get_headline(source, api_key):
    base_url = 'https://newsapi.org/v1/articles?source={}&sortBy=top&apiKey={}'
    url = base_url.format(source, api_key)
    res = requests.get(url)
    json_data = json.loads(res.text)
    descs = []
    #alternatively, title instead of description
    for i in range(len(json_data['articles'])):
        descs.append(json_data['articles'][i]['title'] + ' ')
    return descs
    
def get_all_headlines(api_key):
    rv = []
    for source in SOURCES:
        try:
            rv += get_headline(source, api_key)
        except:
            print('passed on', source)
            pass
    return rv

if __name__ == '__main__':
    api_key = read_api_key()
    rv = get_all_headlines(api_key)
