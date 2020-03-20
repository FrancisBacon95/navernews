# -*- coding: utf-8 -*-
import scrapy

from Naver.items import NaverNews
from Naver.utils import get_content
from Naver.information import Information
import re

# 언론사 및 검색어는 하나만 선택할 경우 with~ 부터 for문 안쪽의 yield 까지 주석 처리후 information.py에서 url 조합 후 start_request의 마지막 yield 해제
# 상세 검색을 사용하고 싶은 경우 상세검색용 url 사용

class NewsSpider(scrapy.Spider):
    name = 'pc'
    
    def start_requests(self):

        # 하나씩만 검색하고 싶은 경우는 반복문부터 주석처리 후 밑에 주석추리된 yield 주석 해제 
        # 언론사 코드 번호는 information.py 혹은 언론사.txt 파일에 정리되어 있음
        
        basic_url='https://search.naver.com/search.naver?&where=news&query='
        url_1="&sort="
        url_2="&photo="
        url_3='&nso=p:from'
        url_4='to'
        url_5='&refresh_start=1' # 자동 새로고침 옵션이긴한데.. 왜 필요한지 의문
        url_press_search='&mynews=1' #언론사별 검색 활성화
        
        # 검색어 및 검색 시작 날짜, 검색 종료 날짜
        query1='3d scanning'
        sd='20200108' # 검색을 시작할 날짜
        ed='20200108' # 검색을 종료할 날짜
        sort="0" # 0: 관련도순 , 1: 최신순 , 2:오래된 순
        photo="0" # 0: 전체, 1: 포토기사 , 2: 동영상기사, 3: 지면기사, 4: 보도자료
        #press_num='1032'
        
        urls=basic_url+query1+url_1+sort+url_2+photo+url_3+sd+url_4+ed+url_press_search
        
        
        # 상세검색 옵션
    
        # 정확히 일치하는 단어 검색
        query2='"CPU"' # 큰 따옴표로 단어를 감싸서 검색해야함
        # 반드시 포함하는 단어검색
        query3='+%2B'+'가격' # 뒤의 작은따옴표에 들어가면됨
        #제외하는 단어
        query4='+-'+'AMD' #뒤의 작은따옴표에 들어가면됨
    
        query=query1+query2+query3+query4
    
        #상세검색 옵션 사용을 위한 url임
        urls_detail=basic_url+query+url_1+sort+url_2+photo+url_3+sd+url_4+ed
        
        with open("Naver/언론사.txt.",'r',encoding='utf-8') as f:
            press_lists=f.read().splitlines()
            
        with open("Naver/KIPOST 수집대상 키워드 목록.txt","r",encoding='utf-8') as f:
            query_list=f.read().splitlines()
        
        for query1 in query_list:
            
            urls=basic_url+query1+url_1+sort+url_2+photo+url_3+sd+url_4+ed+url_press_search
          
            for i in range(1,len(press_lists)):
                press_num=press_lists[i][-4:]
                name=press_lists[i][:-5]
                
                # 언론사 선택은 url의 변화가 아니기 때문에 cookie를 보내서 선택을 해줘야함. 또한 meta에 dont_merge_cookies 를 Fasle로 안하면 안보내짐
                yield scrapy.Request(url=urls,callback=self.parse,cookies={'news_office_checked':press_num},meta={'dont_merge_cookies': False})        
    
        
        #yield scrapy.Request(url=Information.urls,callback=self.parse,cookies={'news_office_checked':'1032'},meta={'dont_merge_cookies': False})
        


    def parse(self, response):
        
        for url,pub,dates,title in zip(response.css('a._sp_each_title::attr(href)').extract(),response.css('._sp_each_source::text').extract(),response.css('dd.txt_inline::text').re(r'\d{4}.\d{2}.\d{2}'),response.css('a._sp_each_title::attr(title)').extract()):
            
            if 'zdnet' not in url:
                
                # TCP timeout error 로 인하여 걸러냄
                
                yield scrapy.Request(url,callback=self.parse_page,meta={'pub_date':dates,'publisher':pub})
        
            
            next_page=response.css('a.next ::attr(href)').extract_first()
            
            if next_page:
                 yield scrapy.Request(response.url+re.sub('&cluster_rank=\d+','',next_page))
                
            
            
    def parse_page(self,response):
        item=NaverNews()
        item['title']=response.css('head title::text').extract_first()
        item['content']=get_content(response.text)
        dates=response.meta['pub_date'].replace('.','-')
        item['pub_date']=dates
        item['url']=response.url
        item['publisher']=response.meta['publisher']
        
        yield item
             
