# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 14:18:58 2017

@author: lin
"""
import time
from tokens import *
from store_hash_table import *
from simhash_128bit import *

jt = JiebaTokenizer('D:/stopword', 'c')

hash_table = store_hash_table('D:/hash_code_file')

def hammingdist(bit_48_query_string,bit_48_hash_table_arr):
    bit_48_query = bit_48_query_string.split('|')[1]
    post_id_dist_dic = {}
    for bit_48 in bit_48_hash_table_arr:
        post_id = bit_48.split('|')[0]
        A_B_hash = zip(bit_48_query,bit_48.split('|')[1])
        cnt = 0
        for A_B in A_B_hash:
            if A_B[0] != A_B[1]:
                cnt += 1
        post_id_dist_dic[post_id] = cnt
    
    dict_sorted= sorted(post_id_dist_dic.items(), key=lambda d:d[1])
    return [elem for elem in dict_sorted if elem[1] < 15]

def find_sim_doc(query):
    query_split_dic = parse_code(query)
    post_id_dist = []
    for bit_16 in query_split_dic.keys():
        if bit_16 in hash_table.keys():
            bit_48_query = query_split_dic[bit_16]
            bit_48_hash_table = hash_table[bit_16]
            arr = hammingdist(bit_48_query,bit_48_hash_table)
            post_id_dist.extend(arr)
        else:
            continue
    return post_id_dist
if __name__ == '__main__':
    doc = ''
    doc_token = jt.tokens(doc)
    query_binary_hash = simhash(doc_token.strip())
    start_time = int(round(time.time()*1000))
    sim_res = find_sim_doc(query_binary_hash)
    end_time = int(round(time.time()*1000))
    print start_time - end_time