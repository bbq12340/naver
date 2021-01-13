# Naver Real Estate Scraper

main.py
  - ui.py
  - worker.py
    - NaverLandScraper.py
    
# NaverLandScraper.py
  1. set query boundary from naver.map
  2. requests for items in the boundary from naver.land -> asList
  3. for item in List:
      scrape each item's (detail, school. articles)
      some items don't have articles. leaves it blank.
  4. returns DF
  
