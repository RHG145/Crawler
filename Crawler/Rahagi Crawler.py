import json
from requests_html import HTMLSession

url = 'http://ejournal.ust.ac.id/index.php/JTIUST/issue/view/265'

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=1)

articles = r.html.xpath('/html/body/div/div[1]/div[1]/div/div/div[2]/div/ul', first=True) #ambil XPath dari <ul class="cmp_article_list articles">

output = []

count = 1

for item in articles.absolute_links:
    r = s.get(item)

    try:
        judul = r.html.find('h1.page_title', first=True).text
    except:
        judul = 'no judul'
    
    try:
        abstract = r.html.find('section.item.abstract', first=True).text
    except:
        abstract = 'no abstract'
    
    try:
        keywords = r.html.find('span.value', first=True).text
    except:
        keywords = 'no keywords'
        
    article_data = {
        'Link': item,
        f'{count} Judul': judul,
        f'{count + 1} Abstract': abstract,
        f'{count + 2} Keywords': keywords
    }
    output.append(article_data)

    count += 3

with open('output.json', 'w') as f:
    json.dump(output, f, indent=4)

print('Output has been saved to output.json')
