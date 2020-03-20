# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class MongoPipeline(object):
    '''
    Item을 몽고 DB에 저장하는 파이프라인
    '''
    
    def __init__(self):
        self.client=MongoClient('mongodb+srv://yuwon:john119@cluster0-hydoh.mongodb.net/test',27071)
        # yuwon 데이터베이스 추출
        self.db=self.client['yuwon']
        # Naver 콜렉션을 추출
        self.collection=self.db['Naver']
        self.items=[]
        
    
    def process_item(self, item, spider):
        '''
        item을 콜렉션에 추가
        '''
        
        compare=self.collection.find_one({"url":item['url']})
        
        if not compare:
#             self.items.append(dict(item))
            self.collection.insert_one(dict(item))
        
        
#         if len(self.items) >= 100:
#             self.insert_current_items()
        
        return item
    
    
#     def insert_current_items(self):
#         items=self.items
#         self.items=[]
        # insert_one()은 한개씩 DB에 전달 many는 여러개 한방에 전달

#         self.collection.insert_many(items)
#         self.collection.insert(items)
#         self.collection.insert_one(items)


    def close_spider(self,spider):
        '''
        spider가 종료될때 호출하여 접속 끊음
        '''
        #현재까지 모아놓은거 저장
#         self.insert_current_items()
        self.client.close()
        