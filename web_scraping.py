from bs4 import BeautifulSoup
import requests

"""Declaración de url's"""
american_banker_url = "https://www.americanbanker.com/"
market_watch_url = "https://www.marketwatch.com/"
el_cronista_url = "https://www.cronista.com/"

# Here, we're just importing both Beautiful Soup and the Requests library
page_link = 'the_url_you_want_to_scrape.scrape_it_real_good.com'
# this is the url that we've already determined is safe and legal to scrape from.
page_response = requests.get(page_link, timeout=5)
# here, we fetch the content from the url, using the requests library
page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.
textContent = []
for i in range(0, 20):
    paragraphs = page_content.find_all("p")[i].text
    textContent.append(paragraphs)
# In my use case, I want to store the speech data I mentioned earlier.  so in this example, I loop through the paragraphs, and push them into an array so that I can manipulate and do fun stuff with the data.
print(page_content.title)
# <title>Returns title tags and the content between the tags</title>
print(page_content.title.string)
# u'Returns the content inside a title tag as a string'
print(page_content.p)
# <p class="title"><b>This returns everything inside the paragraph tag</b></p>
print(page_content.p['class'])
# u'className' (this returns the class name of the element)
print(page_content.a)
# <a class="link" href="http://example.com/example" id="link1">This would return the first matching anchor tag</a>
page_content.find_all('a')
# [<a class="link" href="http://example.com/example1" id="link1">link2</a>,
#  <a class="link" href="http://example.com/example2" id="link2">like3</a>,
#  <a class="link" href="http://example.com/example3" id="link3">Link1</a>]
page_content.find(id="link3")
# <a class="link" href="http://example.com/example3" id="link3">This returns just the matching element by ID</a>
page_content.findAll('div', attrs={"class":"cool_paragraph"})