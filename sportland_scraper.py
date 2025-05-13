from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Product:
    def __init__(self, name="", price="", brand="", link="", sku=None):
        self._name = name
        self._price = price
        self._brand = brand
        self._link = link
        self._sku = sku

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        self._sku = value

    def to_dict(self):
        return {
            'name': self._name,
            'price': self._price,
            'brand': self._brand,
            'link': self._link,
            'sku': self._sku
        }

    def __str__(self):
        return f"Product(name='{self._name}', brand='{self._brand}', price='{self._price}', sku='{self._sku}')"

class ProductList:
    def __init__(self):
        self._products = []

    def add_product(self, product):
        if isinstance(product, Product):
            self._products.append(product)

    def to_dict_list(self):
        return [product.to_dict() for product in self._products]

    def __iter__(self):
        return iter(self._products)

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
            product_list = ProductList()
            for product in products:
                try:
                    # Find the content div that contains name and price
                    content = product.find_element(By.CSS_SELECTOR, ".ProductCard-Content_Base .ProductCard-Content")
                    price_element = product.find_element(By.CSS_SELECTOR, ".ProductPrice ins data")
                    
                    product_data = Product(
                        name=content.find_element(By.CLASS_NAME, "ProductCard-Name").text,
                        price=price_element.get_attribute("value"),
                        brand=content.find_element(By.CLASS_NAME, "ProductCard-Brand").text,
                        link=product.find_element(By.CSS_SELECTOR, "a.ProductCard-Link").get_attribute('href')
                    )
                    product_list.add_product(product_data)
                except Exception as e:
                    print(f"Kļūda iegūstot produkta pamatinformāciju: {str(e)}")
                    continue

            # Tagad apmeklējam katru produkta lapu, lai iegūtu SKU
            for product in product_list:
                try:
                    sku = self.get_product_sku(product.link)
                    if sku:
                        product.sku = sku
                except Exception as e:
                    print(f"Kļūda iegūstot produkta SKU: {str(e)}")
                    continue

            return product_list.to_dict_list()
        except Exception as e:
            print(f"Kļūda iegūstot produktus: {str(e)}")
            return []
        finally:
            self.driver.quit()

