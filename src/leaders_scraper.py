import json
import re
import requests
from bs4 import BeautifulSoup

class WikipediaScraper :

    def __init__(self, base_url : str =' https://country-leaders.onrender.com/') :
        self.base_url= base_url
        self.country_endpoint = base_url+"/countries"
        self.leaders_endpoint = base_url+"/leaders"
        self.cookies_endpoint = base_url+"/cookie"
        self.leaders_data = {}
        self.cookie = requests.get(self.cookies_endpoint).cookies

    def refresh_cookie(self) -> object :
        return requests.get(self.cookies_endpoint).cookies
    
    def get_countries(self) -> list :
        return requests.get(self.country_endpoint, cookies=self.cookie).json()
    
    def get_leaders(self) -> None :
        self.leaders_per_data = []
        countries = self.get_countries()
        for country in countries : 
            req = requests.get(self.leaders_endpoint, cookies=self.cookie, params={'country' : country})
            self.leaders_per_data.append(req.json())
            return self.leaders_per_data

    def get_first_paragraph(wikipedia_url : str) -> None : 
        wikipedia_url = requests.get(wikipedia_url)
        soup_for_paragraph1 = BeautifulSoup(wikipedia_url.text, 'html.parser')
        first_paragraph = []
        for p in soup_for_paragraph1.find_all("p") :
            if p.find("b") : 
                first_paragraph.append(p)
                break
        paragraph_text = "".join(p.get_text() for p in first_paragraph)
        cleaned_first_paragraph = re.sub(r"<[^>]*>","", paragraph_text)
        return cleaned_first_paragraph
    
    def to_json_file(self, filepath : str) -> None :
        with open('leader_data.json', "a", encoding="utf-8") as j:
            json.dump(self.leaders_per_data, j, indent=4, ensure_ascii= False )

    
"""
____________________________________________________________________________
sub_list = []
for country_list in leaders_per_country:
    for leader in country_list:
        sub_list.append(leader)

wikipedia_urls = []
for leader in sub_list:
    if 'wikipedia_url' in leader:
        wikipedia_urls.append(leader['wikipedia_url'])
leaders_first_paragraph = [get_first_paragraph(wikipedia) for wikipedia in wikipedia_urls]
print(leaders_first_paragraph)
"""

