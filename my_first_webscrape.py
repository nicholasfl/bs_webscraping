from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/p/pl?d=graphics+cards'
# opening up connection, grabbing page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"item-container"})

filename = "products.csv"
f = open(filename,"w")
headers = "Brand, Product Name, Shipping\n"

f.write(headers)


for container in containers:
	try:
		container.div.div.a.img["title"]
	except:
		brand = "UNIDENTIFIABLE"
	else:
		brand = container.div.div.a.img["title"]

	title_container = container.findAll("a",{"class":"item-title"})
	product_name = title_container[0].text

	shipping_container = container.findAll("li",{"class":"price-ship"})
	shipping = shipping_container[0].text.strip()

	print("")
	print("Brand: " + brand)
	print("Product Name: " + product_name)
	print("Shipping: " + shipping)
	print("")

	f.write(brand + "," + product_name.replace("," , "|") + "," + shipping + "\n")

f.close()
