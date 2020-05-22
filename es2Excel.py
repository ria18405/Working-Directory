from elasticsearch import Elasticsearch
import csv
import pandas as pd
import requests
import json
def search():
	"""
	Search all data with the index: groupsio_enriched for the attributes like uuid, origin, creation date, body text, subject and projects.
	"""
	#making an elasticsearch object
	es = Elasticsearch()

	"""
 	project_1
 	grimoirelab_creation_date
 	project
	uuid
 	origin
 	Scms_body_extract
 	Scms_Subject_analyzed


	"""

	res = es.search(index="scmspipermail_chaoss_enriched", body={"query": {"match_all": {}}})
	dict_data=[]
	res=res['hits']['hits']
	for i in res:
		dict_data.append(i['_source'])

	csv_columns=list(res[0]['_source'].keys())


	with open("output.csv", 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in dict_data:
			writer.writerow(data)

	df = pd.read_csv('output.csv')
	convert_xlsx(df)

def convert_xlsx(df):
	df.to_excel("output.xlsx", index=None)

def main():
	search()
	print("Output files are output.csv and output.xlsx")

if __name__ == "__main__":
    main()
