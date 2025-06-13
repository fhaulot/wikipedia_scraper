from leaders_scraper import WikipediaScraper

scrap = WikipediaScraper()
scrap.get_leaders()
scrap.to_json_file('leader_data.json')


