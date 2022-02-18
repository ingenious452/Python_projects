'''Let You Download icon from: https://icon-icons.com/
    Ways to Download:
    1.Url-> https://icon-icons.com/pack/World-Cup-2014-Country-Flags-Icons/127
    copy -> World-Cup-2014-Country-Flags-Icons/127
    run the program 

    it only work on https://icon-icons.com site so don't go anywhere else '''

import requests
import pprint
import threading
import sys
import pyperclip
from bs4 import BeautifulSoup

# Get links from the sites
name = sys.argv[1]
print(name)
if not name:
    name = pyperclip.paste()

# url to open to get the image urls
url = f'https://icon-icons.com/pack/{name}'

# requesting the webpage
try:
    source = requests.get(url)
except:
    print('[UNABLE TO RETREIVE]'.center(40, '-'))

# creating a soup object
try:
    caveSoup = BeautifulSoup(source.text, 'html5lib')
except:
    print('[UNABLE TO PARSE]'.center(40, '-'))

imageLinks = list()

for value in range(23):
    iconPreview = caveSoup.find('div', id=f'{value}')
    if iconPreview != None:
        imageDiv = iconPreview.find('div', class_='imagen-pinta-resultados')
        imageLink = imageDiv.img['data-original']
        # creating a list of image links
        imageLinks.append(imageLink)
    else:
        continue

pprint.pprint(imageLinks)

#========================================Links retreieved==========================================


# Downloading image files--------------------
def imageDownloader(url):
    try:
        imageSource = requests.get(url)
    except:
        print('[UNABLE TO RETREIVE IMAGES]'.center(50, '-'))
        sys.exit()

    imageName = url.split('/')[7].split('.')[0]

    # downloading the file
    with open(f'{imageName}.ico', 'wb') as imageFile:
        imageFile.write(imageSource.content)
    print(f'{imageName} Downloaded...')
#------------------------------------------------


# Threading the downloading process--------
listThread = list()

# creating threads
for link in imageLinks:
    thread = threading.Thread(target=imageDownloader, args=[link, ])
    thread.start()
    listThread.append(thread)

for thread in listThread:
    thread.join()
#----------------------------------
