import time
from urllib import response
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
Craigslister

should scrape craigslist in multiple cities for a given search query,
and output the data in a cleanly organized CSV file.

It should then scrape over the CSV file for good hits and send an email notification of the following
"""

headers = {
  'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

base_url = "https://seattle.craigslist.org/search/mca"
query_string = 'ktm 300'.replace(' ', '+')

posts = []

for i in range(0, 5000, 120):
  params = {
    'query': query_string,
    's' : i
  }
  
  response = requests.get(base_url, params=params, headers=headers )
  if response.status_code != 200:
    print('failed api call, status code not 200')
    break
  
  soup = BeautifulSoup(response.content, 'html.parser')
  
  if soup.find('pre', {'id': 'moon'}):
    break
  

  search_results = soup.find('ul', {'id': 'search-results', 'class': 'rows'})
  listings = search_results.find_all('li', 'result_row')
  
  for listing in listings:
    post_url = listing.a['href']
    print(f'Processing post {post_url} . . .')
    
    result_info = listings.div
    post_id = result_info.h3.a['id']
    post_title = result_info.h3.a.text.strip()
    
    location = result_info.find('span', 'result-hood').text.\
      replace('(','').\
      replace('.)','').strip()
      
    picture = True if result_info.find('span', 'pictag') else False
    posts.append([post_id, post_title, location, picture, post_url])
    time.sleep(0.5)
    
df = pd.DataFrame(posts, columns=['Post id', 'Post Title', 'Location', 'Picture', 'Post url'])
df.to_csv('f{query_string}.csv', index=False)