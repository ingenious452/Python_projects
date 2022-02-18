"""
Define article class
"""

import os
import string


class Article:
    """Definae a news class article from nature.com sites"""
    def __init__(self, article_title: str, article_content: str, page_no: int) -> None:
        self._article_title = article_title
        self._article_content = article_content
        self._page_no = page_no

    def parse_article(self) -> str:
        """Replace space with underscore in head and remove 
        trailing whitespace in head and content."""

        self._article_title = self._article_title.strip()
        trantab = str.maketrans(' ', '_', string.punctuation)
        self._article_title = self._article_title.translate(trantab)
        
        self._article_content = self._article_content.strip()

    def save(self):
        """Save the article inside directory named Page_{_page_no}
        with file name _article_head."""
        if self._article_title and self._article_content:
            self.parse_article()  # removing white space and punctuation from head and content
            dir_path = os.path.join(os.getcwd(), f'Page_{self._page_no}')
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            
            file_path = os.path.join(dir_path, f'{self._article_title}.txt')
            with open(file_path, mode='wb') as file:    # encoding is not specified cause binary data is being saved
                file.write(self._article_content)
                                                    
            print(f'Article: {self._article_title} | saved.')
        else:
            print('Heading or content missing.')
    

  