from bs4 import BeautifulSoup
import requests
import csv
# r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# url = 'https://www.cdn.geeksforgeeks.org/page'

# for page in range(2, 10):

#     req = requests.get(url + str(page) + '/')


# # print(r.url)
# # print(r.status_code)
# # print(r.content)

# # Create a beautifulSoup object and specify the parser library
#     soup = BeautifulSoup(req.text, 'html.parser')
#     titles = soup.find_all('div', attrs={'class', 'head'})
#     for i in range(4, 19):
#         if page > 1:
#             print(f"{(i-3)+page*15}" + titles[i].text)
#         else:
#             print(f"{i-3}" + titles[i].text)
# print(soup.prettify())

# print the page title or title tag
# print(soup.title)

# getting the name of the tag
# print(soup.title.name)

# getting the name of the parent tag
# print(soup.title.parent.name)

# find the tag div which holds the class entry-content
# s = soup.find('div', class_='entry-content')

# find all the p tags in the above div
# lines = s.find_all('p')

# to extract the text only in all the p tags
# for line in lines:
#     print(line.text)

# # get tag by id name
# s = soup.find('div', id='main')

# # # get the ul by class name
# leftBar = s.find('ul', class_='leftBarList')

# # # get all the li items
# Content = leftBar.find_all('li')

# for line in Content:
#     print(line.text)
# print(Content)


# For Extracting links
# for link in soup.find_all('a'):
#     print(link.get('href'))


# extract all images from the webpage

# images_list = []

# images = soup.select('img')
# for image in images:
#     src = image.get('src')
#     alt = image.get('alt')
#     images_list.append({'src': src, 'alt': alt})

# for image in images_list:
#     print(image)

# extract the div that has the class = 'head'
# titles = soup.find_all('div', attrs={'class', 'head'})
# print(titles[1].text)


# URL = ['https://www.geeksforgeeks.org/page/2/',
#        'https://www.geeksforgeeks.org/page/10/']

# for url in range(0, 2):
#     req = requests.get(URL[url])
#     soup = BeautifulSoup(req.text, 'html.parser')

#     titles = soup.find_all('div', attrs={'class', 'head'})
#     for i in range(4, 19):
#         if url+1 > 1:
#             print(f"{(i - 3) + url * 15}" + titles[i].text)
#         else:
#             print(f"{i - 3}" + titles[i].text)

URL = 'https://www.geeksforgeeks.org/page/2/'
req = requests.get(URL)
soup = BeautifulSoup(req.text, 'html.parser')

titles = soup.find_all('div', attrs={'class', 'head'})
titles_list = []

count = 1
for title in titles:
    d = {}
    d['Title Number'] = f'title {count}'
    d['Title Name'] = title.text
    count += 1
    titles_list.append(d)

filename = 'Titles.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['Title Number', 'Title Name'])
    w.writeheader()
    w.writerows(titles_list)
