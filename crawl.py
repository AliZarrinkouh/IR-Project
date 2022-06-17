import requests
from bs4 import BeautifulSoup 
from newspaper import Article
from tqdm import tqdm
import pandas as pd
    
def scrap_page(page : int):
    scraped_data = []
    url_list = []
    while page<=91:
        main_page_url = f"http://www.espn.com/sports/soccer/blog/_/name/soccer/count/{page}"
      
         
        html = requests.get(main_page_url).text

        soup = BeautifulSoup(html, features='lxml')
        links = soup.find_all('h3')
        for link in tqdm(links):
            page_url = 'http:'+link.a['href']
            url_list.append(link.a['href'])
            try:
                article = Article(page_url)  
                article.download()
                article.parse()
                print (article.title)
                scraped_data.append({'url' : page_url, 'title' : article.title, 'text' : article.text}) 
            except:
                print(f"failed to process page: {page_url}")
        page += 10                    
    df = pd.DataFrame(scraped_data)
    df.to_csv(f'espn.csv')
    
scrap_page(1)

 
