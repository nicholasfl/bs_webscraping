from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# asking for user input for site search and creating file name and search query from the input
print("\n"+"Welcome to the newegg.com webscraper!" + "\n")
search_query_input = input("What item would you like to search for? ")
search_query = search_query_input.replace(" ","+")
search_query_file_name = search_query_input.replace(" ","_")

print("Creating search query for " + search_query + "..." + "\n")

# creating .csv file
filename = search_query_file_name + "_products.csv"
f = open(filename,"w")
headers = "Brand, Product Name, Shipping\n"

f.write(headers)
base_url = "https://www.newegg.com/p/pl?d=" + search_query
last_part = "&page="
my_url_list = []

# Setting up initial temporary request to find how many pages need to be looped over
page_finder_uClient = uReq(base_url+last_part+"1")
page_finder_page_html = page_finder_uClient.read()
page_finder_uClient.close()
page_finder_page_soup = soup(page_finder_page_html, "html.parser")
page_finder = page_finder_page_soup.findAll("div",{"class":"list-tool-pagination"})
tmp = page_finder[0].strong.text
pages = int(tmp[2:])
print("The amount of pages in search query is " + str(pages) + "\n")

# looping to add each individual website into search list
for num in range(1,pages):
	my_url_list.append(base_url + last_part + str(num))

item_count = 0
for i in range(len(my_url_list)):

	# opening up connection, grabbing page
	uClient = uReq(my_url_list[i])
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")

	# grabs each product
	containers = page_soup.findAll("div",{"class":"item-container"})

	# handling any exceptions where the criteria cannot be found and replacing with N/A
	for container in containers:
		try:
			container.div.div.a.img["title"]
		except:
			brand = "N/A"
		else:
			brand = container.div.div.a.img["title"]

		try:
			title_container = container.findAll("a",{"class":"item-title"})
			product_name = title_container[0].text
		except:
			product_name = "N/A"
		else:
			title_container = container.findAll("a",{"class":"item-title"})
			product_name = title_container[0].text

		try:
			shipping_container = container.findAll("li",{"class":"price-ship"})
			shipping = shipping_container[0].text.strip()
		except:
			shipping = "N/A"
		else:
			shipping_container = container.findAll("li",{"class":"price-ship"})
			shipping = shipping_container[0].text.strip()


		# writing to csv file
		f.write(brand + "," + product_name.replace("," , "|") + "," + shipping + "\n")
		item_count += 1

	f.write("\n")

	percentage_completion = str(i/pages*100)
	print("Search query " + percentage_completion[:4] + "%" + " complete")

f.close()
print("\n" + "Search query complete! Item count: " + str(item_count) + "\n")