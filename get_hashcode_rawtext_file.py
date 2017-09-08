# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

post_id = []
raw_text = []
with open('../lsh_data/yeb_post.data') as comment_file:
	for line in comment_file:
		post_id.append(line.strip().split('$&&$')[0])
		raw_text.append(line.strip().split('$&&$')[1])
df_a = pd.DataFrame({'post_id':post_id,'raw_text':raw_text})


hash_post_id = []
hash_code = []
with open('../lsh_data/yeb_post_hash_code_file') as hash_code_file:
	for line in hash_code_file:
		hash_post_id.append(line.strip().split('\t')[0])
		hash_code.append(line.strip().split('\t')[1])

df_b = pd.DataFrame({'post_id':hash_post_id,'hash_code':hash_code})

df_merge = pd.merge(df_a,df_b,how = 'left',on = 'post_id')

info = zip(raw_text,hash_code)
with open('../lsh_data/yeb_post_hash_code_raw_text','w') as hash_code_raw_text:
	res = []
	for elem in info:
		res.append(elem[1] + '\t' + elem[0] + os.linesep)
	hash_code_raw_text.writelines(res)
