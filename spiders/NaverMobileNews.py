# -*- coding: utf-8 -*-
import scrapy

from Naver.items import NaverNews
from Naver.information import Information
from Naver.utils import get_content
import re

# 언론사 및 검색어는 하나만 선택할 경우 with~ 부터 for문 안쪽의 yield 까지 주석 처리후 information.py에서 url 조합 후 start_request의 마지막 yield 해제
# information.py에서 오는 url을 사용하는 경우 뒤의 pub에 있는 언론사 이름도 같이 바꿔줄것
# 상세 검색을 사용하고 싶은 경우 상세검색용 url 사용

class MNewsSpider(scrapy.Spider):
    name = 'mobile'
    
    def start_requests(self):
        
        mobile_url='https://m.search.naver.com/search.naver?where=m_news&query='
        url_press_search='&mynews=1' #언론사별 검색 활성화
        url_press='&news_office_checked='
        
        url_1="&sort="
        url_2="&photo="
        url_3='&nso=p:from'
        url_4='to'
        url_5='&refresh_start=1'
        
        
        #query1='인텔'
        sd='20200108' # 검색을 시작할 날짜
        ed='20200108' # 검색을 종료할 날짜
        sort="0" # 0: 관련도순 , 1: 최신순 , 2:오래된 순
        photo="0" # 0: 전체, 1: 포토기사 , 2: 동영상기사, 3: 지면기사, 4: 보도자료
        # 언론사 번호는 information.py에 정리되어 있음
        #press_num='1032'
        
        # 상세검색 옵션
    
        # 정확히 일치하는 단어 검색
        #query2='"CPU"' # 큰 따옴표로 단어를 감싸서 검색해야함
        # 반드시 포함하는 단어검색
        #query3='+%2B'+'가격' # 뒤의 작은따옴표에 들어가면됨
        #제외하는 단어
        #query4='+-'+'AMD' #뒤의 작은따옴표에 들어가면됨
    
        #query=query1+query2+query3+query4
    
        #상세검색 옵션 사용을 위한 url임
        #m_urls_detail=mobile_url+query+url_1+sort+url_2+photo+url_press_search+url_3+sd+url_4+ed+url_press+press_num
        
        with open("Naver/언론사.txt",'r',encoding='utf-8') as f:
            press_lists=f.read().splitlines()
            
        with open("Naver/KIPOST 수집대상 키워드 목록.txt","r",encoding='utf-8') as f:
            query_list=f.read().splitlines()
        
        for query1 in query_list:
            
            urls=mobile_url+query1+url_1+sort+url_2+photo+url_press_search+url_3+sd+url_4+ed+url_press#+press_num
          
            for i in range(1,len(press_lists)):
                press_num=press_lists[i][-4:]
                name=press_lists[i][:-5]
            
                yield scrapy.Request(url=urls+press_num,callback=self.parse,meta={"pub": name})
        
        #yield scrapy.Request(url=Information.m_urls,callback=self.parse,meta={"pub": '경향신문'})

    def parse(self, response):

        for url,date in zip(response.css('a.news_tit::attr(href)').extract(),response.css('.sub_txt.sub_time::text').extract()):
            
            pub=response.meta['pub']
            
            if 'thebell' in url:
                # 더벨 같은 경우는 링크와 실제로 연결되는 주소가 다르기 때문에 문서번호를 이용해 실제 연결되는 주소로 바꿔줌
                key=re.search(r'key=\d+$',url)
                key_num=key.group()
                thebell_base='http://m.thebell.co.kr/m/newsview.asp?svccode=00&news'
                
                yield scrapy.Request(thebell_base+key_num,callback=self.parse_page,meta={'pub':pub,'date':date})
            
            else:
                yield scrapy.Request(url,callback=self.parse_page,meta={'pub':pub,'date':date})

            
            more_page=response.css('a.pgn::attr(href)').extract()
            
            if more_page:
                for index in range(1,len(more_page)):
                    yield scrapy.Request(mobile_url[:-20]+re.sub('&cluster_rank=\d+','',more_page[index]),meta={'pub':pub})
                
    def parse_page(self,response):
        item=NaverNews()
        
        if 'naver.com' not in response.url:
        
            if 'thebell' in response.url:
                item['title']=response.css('.tit_view::text').extract_first()
                content=response.css('#DivArticleContent::text').extract()
                content=" ".join(content)
                item['content']=re.sub('[\t\r\n]','',content)

            elif 'ebn' in response.url:
                item['title']=response.css('head title ::text').extract_first()
                body=response.css('#CmAdContent ::text').extract()
                body=" ".join(body)
                item['content']=re.sub('[\t\r\n]','',body)
                
            elif 'hellot' in response.url:
                item['title']=re.sub('[\t\r\n]','',response.css('head title ::text').extract_first())
                body=response.css('#articleBody p::text').extract()
                body=" ".join(body)
                item['content']=re.sub('[\t\r\n]','',body)
                
            
        else:    
            item['title']=response.css('head title ::text').extract_first()
            
            if 'sports' in response.url:
                body=response.css('.main_article::text').extract()
                body=" ".join(body)
                item['content']=re.sub('[\t\r\n]','',body)
            
            else:
                content="".join(response.css('#dic_area::text').extract())
                item['content']=re.sub('[\t\r\n]','',content)
            
            
        date=response.meta['date'].replace('.','-')[:-1]
        item['pub_date']=date
        
        item['url']=response.url
        item['publisher']=response.meta['pub']
        
        yield item