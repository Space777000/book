from django.shortcuts import render
from django.views.generic import View
from .forms import SearchForm
import json
import requests
import os


appid = os.getenv('appid')
SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=' + appid



def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params)
    #print(api.status_code)
    result = json.loads(api.text)
    #items = result['Items']
    return result


class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        
        return render(request, 'app/index.html', {
            'form': form,
        })
        
    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        
        if form.is_valid():
            keyword = form.cleaned_data['title']
            params = {
                'title': keyword,
                'hits': 28,
            }
            result = get_api_data(params)
            items = result['Items']
            book_data = []
            for i in items:
                item = i['Item']
                title = item['title']
                image = item['largeImageUrl']
                isbn = item['isbn']
                query = {
                    'title': title,
                    'image': image,
                    'isbn': isbn,
                }
                book_data.append(query)
              
            page = result['page']       ## 現在のページ
            count = result['count']     ## 検索総数
            pageCount = result['pageCount']  ## 総ページ数
            for_range = [i for i in range(1,pageCount+1)]   
            endnowpage = pageCount - page 
            count_one_s = (page-1) * 28 + 1 
            count_one_e = count_one_s + len(items) -1 
                     
            return render(request, 'app/book.html', {
                'book_data': book_data,
                'keyword': keyword,
                'page': page,
                'count': count,
                'pageCount': pageCount,
                'for_range':for_range,
                'endnowpage':endnowpage,
                'count_one_s':count_one_s,
                'count_one_e':count_one_e,
            })
            
        return  render(request, 'app/index.html', {
            'form': form
        })

class DetailView(View):
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']
        params = {
            'isbn': isbn
        }
        
        result = get_api_data(params)
        items = result['Items']
        items = items[0]
        item = items['Item']
        title = item['title']
        image = item['largeImageUrl']
        author = item['author']
        itemPrice = item['itemPrice']
        salesDate = item['salesDate']
        publisherName = item['publisherName']
        size = item['size']
        isbn = item['isbn']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']
        
        book_data = {
            'title': title,
            'image': image,
            'author': author,
            'itemPrice': itemPrice,
            'salesDate': salesDate,
            'publisherName': publisherName,            
            'size': size,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount,   
            'average': float(reviewAverage) * 20,     
        }
        
        return render(request, 'app/detail.html', {
            'book_data': book_data
        })
        
class BooksView(View):
    def get(self, request, *args, **kwargs):
        page_num = self.kwargs['page_num']
        keyword = self.kwargs['keyword']
        params = {
            'title': keyword,
            'hits': 28,
            'page': page_num,
        }
        result = get_api_data(params)
        items = result['Items']
        book_data = []
        for i in items:
            item = i['Item']
            title = item['title']
            image = item['largeImageUrl']
            isbn = item['isbn']
            query = {
                'title': title,
                'image': image,
                'isbn': isbn,
            }
            book_data.append(query)
                
        page = result['page']       ## 現在のページ
        count = result['count']     ## 検索総数
        pageCount = result['pageCount']  ## 総ページ数
        for_range = [i for i in range(1,pageCount+1)]
        endnowpage = pageCount - page
        count_one_s = (page-1) * 28 + 1 
        count_one_e = count_one_s + len(items) -1
        print(f'差分:{endnowpage}')
        print(f'page:{page}')    
        return render(request, 'app/book.html', {
            'book_data': book_data,
            'keyword': keyword,
            'page': page,
            'count': count,
            'pageCount': pageCount,
            'for_range':for_range,
            'endnowpage':endnowpage,
            'count_one_s': count_one_s,
            'count_one_e': count_one_e,            
            
        })
                        