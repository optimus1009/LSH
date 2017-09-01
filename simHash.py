# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 14:18:58 2017
@author: lin
"""
import os
import time
from tokens import *
from store_hash_table import *
from simhash_128bit import *
comment_post_id = []
comment_raw_data = []
with open('/home/lin.xiong/lsh_data/lsh.data','r') as comment_file:
        for line in comment_file:
            comment_post_id.append(line.strip().split('$&&$')[0])
            comment_raw_data.append(line.strip().split('$&&$')[1])
tup = zip(comment_post_id,comment_raw_data)
post_id_raw_data = dict(tup)
jt = JiebaTokenizer('../lsh_data/stopwords.txt', 'c')

hash_table = store_hash_table('../lsh_data/hash_code_file')
print 'build hash_table success ,and hash_table size is : ',len(hash_table)
def hammingdist(bit_48_query_string,bit_48_hash_table_arr):
    bit_48_query = bit_48_query_string[0].split('|')[1]
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
    return [elem for elem in dict_sorted if elem[1] < 3]   #返回的数据形态 ：[(post_id,dist),]

def find_sim_doc(query):
    query_split_dic = parse_code(query)
    post_id_dist = []
    for bit_16 in query_split_dic.keys():
        if bit_16 in hash_table.keys():
            bit_48_query = query_split_dic[bit_16] # bit_48_auery 是一个数组
            bit_48_hash_table = hash_table[bit_16] # bit_48_hash_table 是一个数组
            arr = hammingdist(bit_48_query,bit_48_hash_table)
            post_id_dist.extend(arr)
        else:
            continue
    return post_id_dist #返回的数据形态 [(post_id,dist),......................]且距离都小于15
if __name__ == '__main__':

    simhashcode = []
    with open('../lsh_data/doc_2.data','r') as token:
        for line in token:
            post_id = line.split('\t')[0]
            doc = line.split('\t')[1]
            binary_hash = simhash(doc.strip())
            simhashcode.append(post_id + '\t' + str(binary_hash))
    #此处需要改造，变成单条数据
    arr = []
    for query_binary_hash in simhashcode:
        print query_binary_hash
        start_time = int(round(time.time()*1000))
        sim_res = find_sim_doc(query_binary_hash) # query_binary_hash: post_id      101010001010101010100010010101010101010100020101001010111100
        end_time = int(round(time.time()*1000))
        cost_time = end_time - start_time
        for elem in sim_res:
            arr.append(post_id_raw_data[elem[0]] +'\t' + str(elem[1]) + os.linesep)
        print 'const time: ',cost_time
    with open('../lsh_data/test_new_tech.data','w') as out:
        out.writelines(arr)
    print 'write res into file success..........'

