# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 21:06:07 2017

@author: lin
"""
import os
import re
import sys

mode_digit_alpha = re.compile(r"[0-9a-zA-Z\_]+")
digit_alpha_pattern = re.compile(r"[A-Za-z0-9\[\`\~\!\@\#\$\^\&\?\...\】\【\!\《\》\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\!\@\#\\\&\*\%]")
emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  
    u"(\ud83d[\u0000-\uddff])|"  
    u"(\ud83d[\ude80-\udeff])|"  
    u"(\ud83c[\udde0-\uddff])"  
    "+", flags=re.UNICODE)
if __name__ == '__main__':
#    if len(sys.argv) < 2:
#        print 'Usage: need two arguments doc_1.data doc_1_clear.data'
#        exit(-1)
#    input_data,output_data = sys.argv[1:]
    input_data,output_data = ('/home/lin.xiong/text-similarity/data/test.data','/home/lin.xiong/text-similarity/data/python_clear.data')
    clear_text = []
    with open(input_data,'r') as f:
        for line in f.readlines():
            raw_text = unicode(line.strip(),'utf8')
            #raw_text = line.split('\t')[3]
            r_1 = digit_alpha_pattern.sub(r"", raw_text)
            r = emoji_pattern.sub(r'',r_1)
            clear_text.append(r.encode('utf8') + os.linesep)
    with open(output_data,'w') as output:
        output.writelines(clear_text)

