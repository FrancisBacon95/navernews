#!/usr/bin/env python
# coding: utf-8

class Information:
    '''
    url 조합하는 곳
    '''
    
    basic_url='https://search.naver.com/search.naver?&where=news&query='
    url_1="&sort="
    url_2="&photo="
    url_3='&nso=p:from'
    url_4='to'
    url_5='&refresh_start=1'
    
    #모바일 검색 주소
    mobile_url='https://m.search.naver.com/search.naver?where=m_news&query='
    url_press_search='&mynews=1' #언론사별 검색 활성화
    url_press='&news_office_checked='
    
#------------------------------------------------------------------------------------------------------------------#   
    # 검색어 및 검색 시작 날짜, 검색 종료 날짜
    query1='3d scanning'
    sd='20200108' # 검색을 시작할 날짜
    ed='20200109' # 검색을 종료할 날짜
    sort="0" # 0: 관련도순 , 1: 최신순 , 2:오래된 순
    photo="0" # 0: 전체, 1: 포토기사 , 2: 동영상기사, 3: 지면기사, 4: 보도자료
    

    
    urls=basic_url+query1+url_1+sort+url_2+photo+url_3+sd+url_4+ed#+url_5 #(자동 새로고침 활성화를 위해서는 주석 해제)
    nodate_url=basic_url+query1+url_1+sort+url_2+photo
    
    
    # 상세검색 옵션
    
    # 정확히 일치하는 단어 검색
    query2='"CPU"' # 큰 따옴표로 단어를 감싸서 검색해야함
    # 반드시 포함하는 단어검색
    query3='+%2B'+'가격' # 뒤의 작은따옴표에 들어가면됨
    #제외하는 단어
    query4='+-'+'AMD' #뒤의 작은따옴표에 들어가면됨
    
    query=query1+query2+query3+query4
    
    #상세검색 옵션 사용을 위한 url임
    urls_detail=basic_url+query+url_1+sort+url_2+photo+url_3+sd+url_4+ed#+url_5 #(자동 새로고침 활성화를 위해서는 주석 해제)

#-----------------------------------------------------------------------------------------------------------------------#
    # 모바일 검색 
    # 경향신문:1032 , 국민일보:1005 ,  동아일보:1020 , 문화일보:1021, 서울신문:1081, 세계일보:1022, 조선일보:1023, 중앙일보:1025
    # 한겨레:1028, 한국일보:1469 , 매일경제:1009, 머니투데이:1008, 서울경제:1011 , 아시아경제:1277 , 이데일리:1018 , 조선비즈: 1366
    # 조세일보:1123 , 파이낸셜뉴스:1014 , 한국경제:1015 , 헤럴드경제:1016 , YTN:1052 , 디지털데일리:1138 , 디지털타임스:1029
    # 블로터:1293 , 전자신문:1030, ZDNetKorea:1092 , 더벨:2254 , 헬로티:2417 , EBN:2093
    
    # 따로 언론사 하나만 선택해서 넘길 수 있음
    press_num='1032'
    m_urls=mobile_url+query1+url_1+sort+url_2+photo+url_press_search+url_3+sd+url_4+ed+url_press+press_num
    m_urls_detail=mobile_url+query+url_1+sort+url_2+photo+url_press_search+url_3+sd+url_4+ed+url_press+press_num
    