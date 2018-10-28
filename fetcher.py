import json
import urllib.request
import category as cat
from collections import defaultdict
from pathlib import Path
path_str="C:\\Users\\Peter\\Desktop\\malprojectv2\\Json test"
x = Path(path_str)
mal_id_list=set()
trait_dict=defaultdict(int)
anime_trait_dict=dict()
def extract(url):
    #extracts the json data into something useable, returns json file
    response=urllib.request.urlopen(url)
    data=response.read()
    response.close()
    text=data.decode(encoding = 'utf-8)')
    return(json.loads(text))
def searchprint(obj):
    #prints the results of the whole search
    global mal_id_list
    for result in obj['results']:
        print(result['mal_id'],result['title'])
        mal_id_list.add(result['mal_id'])
def anime_extract(obj):
    trait_dict[obj['type']]+=1
    anime_trait_dict[obj['mal_id']]=[]
    anime_trait_dict[obj['mal_id']].append(obj['type'])
    for genre in obj['genres']:
        anime_trait_dict[obj['mal_id']].append(genre['mal_id'])
        trait_dict[genre['mal_id']]+=1
def list_extract(mlist:'list of ids'):
    global trait_dict
    global anime_trait_dict
    trait_dict=defaultdict(int)
    anime_trait_dict=dict()
    for anime in mlist:
        with open(f'Json test//{anime}.json','r') as file:
            anime_dict=json.load(file)
            anime_extract(anime_dict)
def search_folder(score,genre):
    for f in x.iterdir():
        with open(f,'r') as file:
            jfile=json.load(file)
            if type(jfile['score'])== int:
                print(cat.reverse_gd[genre],[x['mal_id'] for x in jfile['genres']])
                if jfile['score'] > score and cat.reverse_gd[genre] in [x['mal_id'] for x in jfile['genres']]:
                    mal_id_list.add(jfile['mal_id'])
                    print(jfile['mal_id'])
def urlcon(score:float,*genre:str):
    #constructs the url using search constraints, currently using two genres first
    url='https://api.jikan.moe/v3/search/anime?'
    for g in sorted(genre):
        if g in cat.reverse_gd:
            url+=f'&genre={cat.reverse_gd[g]}'
    if type(score)==float or type(score)==int:
        url+=f'&score={score}'
    return url
def search_page_extract(url):
    page=0
    global mal_id_list
    mal_id_list=set()
    while True:
        try:
            page+=1
            print(f'page {page}')
            searchprint(extract(url+f'&page={page}'))
        except urllib.error.HTTPError:
            print('None')
            print(len(mal_id_list))
            break
def splicer(trait_dict,mal_id_list):
    return sorted([(key,trait_dict[key]) for key in trait_dict],key=lambda t: abs(len(mal_id_list)/2-t[1]))[0][0]
def narrow_choices():
    #should return a mal_list thats just smaller, would be optimal
    #shouldn't ask the same trait twice
    #although above might not be a problem
    new_list=[]
    trait=splicer(trait_dict,anime_trait_dict)
    if trait in cat.gd:
        trait=cat.gd[trait]
    choice=input(f'{trait}?')
    if choice=='y':
        for anime in anime_trait_dict:
            if trait in cat.reverse_gd:
                if cat.reverse_gd[trait] in anime_trait_dict[anime]:
                    new_list.append(anime)
            else:
                if trait in anime_trait_dict[anime]:
                    new_list.append(anime)
        list_extract(new_list)
    else:
        for anime in anime_trait_dict:
            if trait in cat.reverse_gd:
                if cat.reverse_gd[trait] not in anime_trait_dict[anime]:
                    new_list.append(anime)
            else:
                if trait not in anime_trait_dict[anime]:
                    new_list.append(anime)
        list_extract(new_list)
    print(new_list)
def loop():
    while True:
        narrow_choices()
        
