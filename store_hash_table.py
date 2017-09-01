# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 11:29:00 2017

@author: lin
"""
class TableNode(object):
    def __init__(self, index):
        self.val = index
        self.buckets = {}
def parse_code(post_id_hash_code):
    post_id = post_id_hash_code.strip().split('\t')[0]
    hash_code = post_id_hash_code.strip().split('\t')[1]
    A,B,C,D = (hash_code[0:16],hash_code[16:32],hash_code[32:48],hash_code[48:])
    tmp_dic = {}
    tmp_dic[A] = [post_id + '|' + B+C+D]
    tmp_dic[B] = [post_id + '|' + A+C+D]
    tmp_dic[C] = [post_id + '|' + A+B+D]
    tmp_dic[D] = [post_id + '|' + A+B+C]
    return tmp_dic
def store_hash_table(hash_code_file):
    hash_table = {}
    with open(hash_code_file,'r') as code:
        for line in code:
            split_16_48_dic = parse_code(line)
            for bit_16 in split_16_48_dic.keys():
                if bit_16 in hash_table:
                    hash_table[bit_16].append(split_16_48_dic[bit_16][0])
                else:
                    hash_table[bit_16] = split_16_48_dic[bit_16]
    return hash_table

                    
