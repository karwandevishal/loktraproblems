from bs4 import BeautifulSoup
from  urllib import request as url_request
from  urllib import error as url_error
from urllib import parse as url_parse
import re
import sys
import queue
import threading

def get_page(url):
    """Given a url read it."""
    try:
        html = url_request.urlopen(url).read()
        return html
    except url_error.HTTPError as http_e:
        print('{}'.format(http_e))
        return 'error'
    except url_error.URLError as url_e:
        print('{}'.format(url_e))
        return 'error'
    except Exception as e:
        print(e)
        return 'error'

def extract_result(html, keyword):
    """Given html extract lines with keyword in them."""
    try:
##        print('xxx')
        soup = BeautifulSoup(html, 'html.parser')
##        print(soup)
        form_name = {'name': re.compile('compareprd')}
        form = soup.find(attrs=form_name)
        if form is None:
            return {'error': 'page number does not exists for keyword {}'.format(keyword)}
        children_class = {'class': re.compile('productName')}
        grid_boxes = form.findChildren('a', attrs=children_class)
        result = []
        for children in grid_boxes:
            # children may directly have title or it may have span
            spans = children.findChildren('span')
##            print('xxxxxx {}'.format(spans))
            if len(spans) > 0:
                result.append(spans[0]['title'])
            else:
                result.append(children['title'])
        return result
    except Exception as e:
        print('extract_result {}'.format(e))
        return 'error'

def get_page_count(html):
    """return count of pages in pagination class
       find paginationNew div, find span with class ellips,
       find next sibling with tag a, get text of a
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        pagination_class = {'class': re.compile('paginationNew')}
        total_pages = soup.find(attrs=pagination_class)
        total_pages = total_pages.find('span', attrs={'class': 'ellips'})
        total_pages = total_pages.findNextSiblings('a').pop()
        return int(total_pages.getText())
    except Exception as e:
        print(e)
        return 'error'

def construct_url(keyword, page_number=None):
    """construct url which is going to be used for query."""
    url = 'http://www.shopping.com/products'
    url_parts = list(url_parse.urlparse(url))
    query = url_parse.urlencode({'KW': keyword})
    if page_number is None:
        url_parts[4] = query
        url = url_parse.urlunparse(url_parts)
    else:
        url_parts[2] = url_parts[2] + '~PG-' + str(page_number)
        url_parts[4] = query
        url = url_parse.urlunparse(url_parts)
    return url

def get_final_result(keyword, page_number):
    """Get the result for keyword"""
    if page_number is None:
        # collect from all pages
        url = construct_url(keyword)
        print(url)
        result = []
        html = get_page(url)
        pages = get_page_count(html)
        print(pages)
        tmp = extract_result(html, keyword)
        result.extend(tmp)
        if isinstance(pages, int):
            for page in range(2, pages):
                url = construct_url(keyword, page_number=page)
                tmp = extract_result(html, keyword)
                if isinstance(tmp, list):
                    result.extend(tmp)
        return result
    else:
        url = construct_url(keyword, page_number=page_number)
        print(url)
        html = get_page(url)
##        if keyword == 'trimmer':
##            html = open('trimmer.html', 'r+', encoding='utf8')
##        else:
##        file_name = '.'.join([keyword, 'html'])
##        html = open(file_name, 'r+', encoding='utf8')
        result = extract_result(html, keyword)
        print(len(result))
        return result

    
if __name__ == '__main__':
    arg_len = len(sys.argv)
    print(arg_len)
    if arg_len < 2:
        print('usage: python web_crawler.py keyword [page number]')
        exit(0)
    try:
        keyword = sys.argv[1].strip()
        keyword = keyword.strip("'")
        keyword = keyword.strip('"')
        page_number = None
        if arg_len > 2:
            page_number = int(sys.argv[2].strip())
        result = get_final_result(keyword, page_number)
        print(result)
        print(len(result))
    except ValueError as v_error:
        print('page number should be integer')
    except Exception as e:
        print(e)
    
    

