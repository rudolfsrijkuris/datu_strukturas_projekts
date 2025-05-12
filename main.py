from sportland_scraper import SportlandScraper

scraper = SportlandScraper()
products = scraper.get_products("https://sportland.lv/viriesu/apavi")
print(products)