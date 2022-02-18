'''
Scraping articles from nature.com sites 
Author: ingenious452
Date: 20-10-2021 (dd-mm-yyyy)
'''

# importing the required library
import logging
import requests
import time

from typing import List
from article import Article
from bs4 import BeautifulSoup
from bs4.element import Tag


logging.basicConfig(filename='scrape.log', filemode='w',
                    level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s : %(name)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


class ArticleScraper:
    """Scrap article from: https://www.nature.com/"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.saved_articles = []  
    
    def parse(self, page: bytes) -> BeautifulSoup:
        """Given page html content parse the page using 
        BeautifulSoup and return a soup object.

        :page: bytes: html bytes string to be parsed
        :return: BeautifulSoup: parsed html soup object
        """
        try:
            soup = BeautifulSoup(page, 'html5lib')
        except TypeError as e:
            logging.error('Unable to parse the page.')
            logging.error(e)
            return None
        else:
            logging.debug('Successfully parsed the page.')
            return soup

    def webpage(self, page_no: int) -> bytes:
        """Get the html of the page number at given url.
        
        :page_no:str: page number to retrieve from base_url.
        :return: bytes | None 
        """
        url = ''.join([self.base_url, '/nature/articles'])
        try:
            response = requests.get(url, 
                                    headers={'Accepted-Language': 'en-US,en;q=0.5'},
                                    params={'searchType': 'journalSearch',
                                            'sort': 'PubDate',
                                            'year': '2020',
                                            'page': str(page_no)})
        except requests.ConnectionError as e:
            logging.error(e)
            return None
        else:
            if response.status_code == 200:
                logging.debug(f'Successfully retrieved Page: {page_no} from {response.request.url}')
                return response.content
            else:
                logging.debug(f'Unable to retrieve the page! error: {response.status_code}')
                return None
        
    def article_tags(self, soup_page: BeautifulSoup) -> List[Tag]:
        """Given a parsed html page return all the 
        article tags present in the page.

        :soup_page: parsed BeautifulSoup object
        :return : list of article Tag
        """
        try:
             tags = soup_page.find_all('article')
        except AttributeError as e:
            logging.error(e)
            return []
        except TypeError as e:
            logging.error(e)
            return []
        else:
            logging.debug(f'{len(tags)} articles tags retrieved.')
            return tags

    def article_links(self, article_tags: List[Tag], required_type: str) -> List[str]:
        """Return all news type article from a given articles TagObject

        :param articles: List of article TagObjects
        :return articles_links: List of links to the articles
        """
        links = []
        if article_tags:
            logging.debug('Retreving the article links.')
            for index, article_tag in enumerate(article_tags, start=1):
                logging.info(f'Retreiving {index} article link')
                try:
                    span_tag = article_tag.find('span', {'data-test': 'article.type'})
                    article_type = span_tag.span.string
                    if article_type == required_type:
                        # relative article link will be retreived
                        link = article_tag.find('a', {'data-track-action': 'view article'}).get('href')   
                    else:
                        continue
                except AttributeError as e:
                    print(e)
                    logging.debug(e)
                    continue
                except TypeError as e:
                    print(e)
                    logging.debug(e)
                    continue
                else:
                    links.append(''.join([self.base_url, link]))
                    logging.debug(f'Successfully retreived {required_type} link!') 
            if links:
                logging.debug(f'{len(links)} {required_type} article link retrieved successfully.')
                return links
            else:
                logging.debug(f'No {self.article_type} article present')
                return []   
        else: 
            logging.debug('Given list of article tags is empty.')
            return []

    def article_page(self, article_link: str) -> str:
        """
        Request the given article link and return the html source of that article page.

        :param article_link: str :  article page to be retrieved from url.
        :return: str : html string of the page.
        """
        logging.debug(f'Requesting article: {article_link}')
        try:
            response = requests.get(article_link)
        except requests.ConnectionError as e:
            print(e)
            return None
        else:
            if response.status_code == 200:
                logging.debug(f'Successfully retrieved article page from {response.request.url}')
                return response.content
            else:
                logging.debug(f'Unable to retrieve the article page! error: {response.status_code}')
                return None
    
    def article_title(self, article_page):
        """
        Return the title from the given article page.

        :param article_page: parsed article page whose heading to be retreived.
        :return str: title of the article
        """
        logging.debug(f'Retreiving the article title.')
        try:
            h1 = article_page.find('h1', {'itemprop': 'headline'})
            article_title = h1.string
        except AttributeError as e:
            logging.debug(e)
            return ''
        except TypeError as e:
            logging.debug(e)
            return ''
        else:
            return article_title

    def article_body(self, article_page):
        """"Return the body of the given article page

        :param article: parsed html of the article_page
        :return str: content of the given article
        """
        logging.debug(f'Retreving article content')
        article_body = ''
        try:
            div = article_page.find('div', {'class': 'c-article-body'})
            paragraphs = div.find_all('p')
            # paragraphs = [child for child in div.children if child.name == 'p']
        except AttributeError as e:
            logging.debug(e)
            return ''
        except TypeError as e:
            logging.debug(e)
            return ''
        else:
            article_body = ''.join([paragraph.get_text().strip() for paragraph in paragraphs])
            return article_body.encode('utf-8')

    def crawl(self, pages, type_='News'):
        # range exclude the end number 
        print('Started Crawler'.center(50, '-'))
        try:
            for page in  range(1, pages+1):
                # print(page)
                indexed_page = self.webpage(page)
                parsed_indexed_page = self.parse(indexed_page)
                tags = a.article_tags(parsed_indexed_page)
                
                links = a.article_links(tags, type_)
                for link in links:
                    parse_article_page = self.parse(self.article_page(link))
                    article_heading = a.article_title(parse_article_page)
                    article_body = self.article_body(parse_article_page)
                    article = Article(article_heading, article_body, page)
                    article.save()
                    self.saved_articles.append(article)
                
                    time.sleep(5)  # Wait 5 second after requesting one article page :)
        except KeyboardInterrupt as e:
            print('Crawler halted'.center(50, '-'))
        else:
            print('Crawler Stoped'.center(50, '-'))


a = ArticleScraper('https://www.nature.com')
a.crawl(5)  # specify number of pages to crawl