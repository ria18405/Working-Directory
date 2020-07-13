"""
Input: Tagged output of Github, Mbox,IRC 

Output: Json string

"""
import pandas as pd 
import json
csv_file_df=pd.read_csv("tagged_output.csv")
print(len(csv_file_df))
json_str='['
for i in range(len(csv_file_df)):

	d=json.dumps(csv_file_df['scms_tag'][i])
	print(i)
	d=d[1:-1].replace("\'",'"')
	json_str+='{{"conditions":[{{"field":"id","value":"{0}"}}],"set_extra_fields":[{{"field":"scms_tags","value":{1}}}]}},'.format(csv_file_df['id'][i],d)
	json_str+='{{"conditions":[{{"field":"id","value":"{0}"}}],"set_extra_fields":[{{"field":"Weight","value":{1}}}]}},'.format(csv_file_df['id'][i],int(csv_file_df['Weight'][i]))
	json_str+='{{"conditions":[{{"field":"id","value":"{0}"}}],"set_extra_fields":[{{"field":"Category","value":"{1}"}}]}},'.format(csv_file_df['id'][i],csv_file_df['Category'][i])

json_str=json_str[:-1]+']'


newfile=open("output.json",'w')
newfile.write(json_str)


