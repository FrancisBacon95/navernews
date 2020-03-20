#!/usr/bin/env python
# coding: utf-8

import logging

import lxml.html
import readability 

import re

logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html):
    document=readability.Document(html)
    content_html=document.summary()
    content_text=lxml.html.fromstring(content_html).text_content().strip()
    content_clean=re.sub('[\t\r\n]','',content_text)
    content_strip=" ".join(content_clean.split())
    #content_final=re.sub(r'\D{2}\s\d{4}.\d{2}.\d{2}\s.{5}','',content_strip)
    
    return content_strip

