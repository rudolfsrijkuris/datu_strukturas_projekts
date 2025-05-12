from sportland_scraper import SportlandScraper

scraper = SportlandScraper()
products = scraper.get_products("https://sportland.lv/viriesu/apavi")
# products = scraper.get_products("https://sportland.lv/viriesu/apgerbi")
print(products)