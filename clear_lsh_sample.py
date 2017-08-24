# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 21:06:07 2017

@author: lin
"""

import re
import sys

    
mode_digit_alpha = re.compile(r"[0-9a-zA-Z\_]+")
digit_alpha_pattern = re.compile(r"[A-Za-z0-9\[\`\~\!\@\#\$\^\&\?\...\】\【\!\《\》\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\!\@\#\\\&\*\%]")

emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: need two arguments doc_1.data doc_1_clear.data'
        exit(-1)
    input_data,output_data = sys.argv[1:]
    without_digit_alpht = open(output_data,'w')
    with open(input_data,'r') as f:
        for line in f.readlines():
            raw_text = unicode(line,'utf-8')
            #raw_text = line.split('\t')[3]
            r_1 = digit_alpha_pattern.sub(r"", raw_text)
            r = emoji_pattern.sub(r'',r_1)
            without_digit_alpht.write(r.encode('utf-8') +'\n')
    without_digit_alpht.close()

