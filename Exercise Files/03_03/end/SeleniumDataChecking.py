from selenium import webdriver

driver = webdriver.Chrome()

driver.get('http://www.phptravels.net/offers')

b_tags = driver.find_elements_by_tag_name('b')

price_list = []
for b in b_tags:
    price_list.append(b.text)

clean_price_list =[]
for price in price_list:
    if price.startswith('USD'):
        price_number = price[5:]
        integer_price = int(price_number.replace(',',''))
        clean_price_list.append(integer_price)

print (sorted(clean_price_list))