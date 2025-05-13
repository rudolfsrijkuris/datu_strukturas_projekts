from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time

class Product:
    def __init__(self, name="", price="", brand="", link="", sku=None, sizes=None):
        self._name = name
        self._price = price
        self._brand = brand
        self._link = link
        self._sku = sku
        self._sizes = sizes if sizes is not None else []

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

    @property
    def sizes(self):
        return self._sizes

    @sizes.setter
    def sizes(self, value):
        self._sizes = value

    def to_dict(self):
        return {
            'name': self._name,
            'price': self._price,
            'brand': self._brand,
            'link': self._link,
            'sku': self._sku,
            'sizes': self._sizes
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
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def get_product_details(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)  # Ļauj lapai ielādēties
            
            try:
                # Atrod produkta kodu
                sku_element = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ProductActions-ProductSku"))
                )
                sku_text = sku_element.text.strip()
                sku = sku_text.split('#')[1].strip() if '#' in sku_text else sku_text
                
                # Atrod pieejamos izmērus
                available_sizes = []
                try:
                    size_elements = self.wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, ".ProductAttributeValue:not(.ProductAttributeValue_isNotAvailable) .ProductAttributeValue-StringText")
                        )
                    )
                    available_sizes = [size.text.strip() for size in size_elements if size.text.strip()]
                except TimeoutException:
                    print(f"Brīdinājums: Nav atrasti izmēri produktam {url}")
                
                return sku, available_sizes
                
            except (TimeoutException, NoSuchElementException, IndexError) as e:
                print(f"Brīdinājums: Neizdevās iegūt SKU produktam {url}: {str(e)}")
                return None, []
                
        except Exception as e:
            print(f"Kļūda iegūstot produkta detaļas no {url}: {str(e)}")
            return None, []

    def get_products(self, url):
        try:
            print("Sāku produktu iegūšanu no:", url)
            product_list = ProductList()
            page = 1
            total_products = 0
            
            while True:
                page_url = f"{url}?page={page}"
                print(f"\nApstrādāju {page}. lapu: {page_url}")
                
                try:
                    self.driver.get(page_url)
                    time.sleep(2)  # Ļauj lapai ielādēties
                    
                    try:
                        # Gaida līdz produkti ielādējas
                        products = self.wait.until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductCard"))
                        )
                        
                        if not products:
                            print(f"Lapa {page} ir tukša. Beidzu skrāpēšanu.")
                            break
                        
                        # Apstrādā katru produktu
                        page_products = 0
                        for product in products:
                            try:
                                # Atrod produkta elementus
                                content = product.find_element(By.CSS_SELECTOR, ".ProductCard-Content_Base .ProductCard-Content")
                                
                                # Atrod cenu
                                try:
                                    price_element = product.find_element(By.CSS_SELECTOR, ".ProductPrice ins data")
                                except NoSuchElementException:
                                    try:
                                        price_element = product.find_element(By.CSS_SELECTOR, ".ProductPrice data")
                                    except NoSuchElementException:
                                        print("Neizdevās atrast cenu produktam")
                                        continue
                                
                                # Izveido produkta objektu
                                product_data = Product(
                                    name=content.find_element(By.CLASS_NAME, "ProductCard-Name").text,
                                    price=price_element.get_attribute("value"),
                                    brand=content.find_element(By.CLASS_NAME, "ProductCard-Brand").text,
                                    link=product.find_element(By.CSS_SELECTOR, "a.ProductCard-Link").get_attribute('href')
                                )
                                
                                product_list.add_product(product_data)
                                page_products += 1
                                
                            except Exception as e:
                                print(f"Kļūda apstrādājot produktu: {str(e)}")
                                continue
                        
                        total_products += page_products
                        print(f"No {page}. lapas iegūti {page_products} produkti")
                        print(f"Kopā līdz šim iegūti {total_products} produkti")
                        
                        if page_products == 0:
                            break
                            
                        page += 1
                        
                    except TimeoutException:
                        print(f"Lapa {page} neielādējās. Beidzu skrāpēšanu.")
                        break
                        
                except Exception as e:
                    print(f"Kļūda ielādējot {page}. lapu: {str(e)}")
                    break
            
            print(f"\nKopā iegūti {total_products} produkti no {page-1} lapām")
            
            # Iegūst detalizētu informāciju par katru produktu
            print("\nIegūstu detalizētu informāciju par produktiem...")
            for i, product in enumerate(product_list, 1):
                try:
                    sku, available_sizes = self.get_product_details(product.link)
                    if sku:
                        product.sku = sku
                    product.sizes = available_sizes
                    if i % 5 == 0:
                        print(f"Iegūta detalizēta informācija par {i}/{len(product_list._products)} produktiem")
                except Exception as e:
                    print(f"Kļūda iegūstot produkta {i}/{len(product_list._products)} detaļas: {str(e)}")
                    continue
            
            return product_list.to_dict_list()
            
        except Exception as e:
            print(f"Kļūda iegūstot produktus: {str(e)}")
            return []
        finally:
            self.driver.quit()

