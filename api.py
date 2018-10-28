import fetcher as jf
import category as cat
import json
def ask():
    score=int(input('what is the min score?'))
    genre=str(input('what genre?'))
    url = jf.urlcon(score,genre)
    jf.search_page_extract(url)
#jf.search_folder(9,'comedy')
jf.search_page_extract(jf.urlcon(8,'action'))
jf.list_extract(jf.mal_id_list)
jf.loop()
