from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SportlandScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def get_product_sku(self, url):
        try:
            self.driver.get(url)
            sku_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "ProductActions-ProductSku"))
            )
            # Extract just the SKU code after the '#' symbol
            sku = sku_element.text.split('#')[1].strip()
            return sku
        except Exception as e:
            print(f"Kļūda iegūstot SKU: {str(e)}")
            return None

    def get_products(self, url):
        try:
            self.driver.get(url)

            # Sagaidam, kad produkti ielādējas
            products = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductCard"))
            )

            # Iegūst produktu datus
            product_list = []
            for product in products:
                try:
                    # Find the content div that contains name and price
                    content = product.find_element(By.CSS_SELECTOR, ".ProductCard-Content_Base .ProductCard-Content")
                    price_element = product.find_element(By.CSS_SELECTOR, ".ProductPrice ins data")
                    
                    product_data = {
                        'name': content.find_element(By.CLASS_NAME, "ProductCard-Name").text,
                        'price': price_element.get_attribute("value"),
                        'brand': content.find_element(By.CLASS_NAME, "ProductCard-Brand").text,
                        'link': product.find_element(By.CSS_SELECTOR, "a.ProductCard-Link").get_attribute('href')
                    }
                    product_list.append(product_data)
                except Exception as e:
                    print(f"Kļūda iegūstot produkta pamatinformāciju: {str(e)}")
                    continue

            # Tagad apmeklējam katru produkta lapu, lai iegūtu SKU
            for product_data in product_list:
                try:
                    sku = self.get_product_sku(product_data['link'])
                    if sku:
                        product_data['sku'] = sku
                except Exception as e:
                    print(f"Kļūda iegūstot produkta SKU: {str(e)}")
                    continue

            return product_list
        except Exception as e:
            print(f"Kļūda iegūstot produktus: {str(e)}")
            return []
        finally:
            self.driver.quit()

