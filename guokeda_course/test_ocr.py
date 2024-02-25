# -*- encoding: utf-8 -*-
"""
File test_ocr.py
Created on 2023/9/18 23:39
Copyright (c) 2023/9/18
@author: 
"""
import easyocr

if __name__ == '__main__':
    reader = easyocr.Reader(['ch_sim', 'en'], gpu = False)
    result = reader.readtext('login.png')
    print(result)