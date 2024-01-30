import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from summarizer import summarize_text

summary_data = dict()

def scrape_link(link):
    print(f"Working on link: {link}")
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    summary_data[link] = ' '.join(soup.stripped_strings)

# outline main function
def serp(query=None):
    if query is None:
    # accept keyword from the user
        query = quote_plus(input("Enter space-separated keywords: ").strip())
    else:
        query = quote_plus(query.strip())
    # use keyword to make API call with requests
    print(query)
    path = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyC9-yThffMzzsDYcQN7aZZUyVtre8bySsU&cx=93b7cb032f56c40e2&q={query}"
    resp = requests.get(path)

    resp.raise_for_status()

    if resp.status_code != 200:
        print('Something went wrong with the API call')
        return
    # parse the JSON the api returns and store urls
    data = resp.json()
    print(f'Google searched for {data["queries"]["request"][0]["title"]}')
    search_results = [x["link"] for x in data["items"]]
    print("Google returned, ", search_results) 
    
    # use beautiful soup & requests to 
    # get website content and store in dictionary
    # make scraping process concurrent
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_link, search_results)
    
    # print(summary_data)
    print("The page data is: ")
    for k,v in summary_data.items():
        print(f"Link: {k}, text: {v[0:200]}")
    
    
    with ThreadPoolExecutor() as executor:
        for k,v in summary_data.items():
            future = executor.submit(summarize_text, v)
            summary_data[k] = future.result()
    
    print("The summarized page data is: ")
    for k,v in summary_data.items():
        print(f"Link: {k}, text: {v[0:200]}")
    
    return summary_data

    

if __name__ == "__main__":
    serp()