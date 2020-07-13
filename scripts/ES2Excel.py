"""
This script converts ElasticSearch indexes to 
CSV file,
Excel sheet,
Google Sheets.

Elastic Search indices: 
all_scms (containing Github Mbox and IRC enriched data)



"""
from elasticsearch import Elasticsearch
import csv
import pandas as pd
import requests
import json



def search():
	
	es = Elasticsearch()

	res = es.search(index="all_scms", body={"query": {"match_all": {}}},size=9000)
	dict_data=[]
	
	for hit in res['hits']['hits']:
		dict_data.append(hit['_source'])

	arr_id=[]
	arr_grimoire_creation_date=[]
	arr_context=[]
	arr_body=[]
	arr_channel=[]

	for data in dict_data:
		if("https://coveralls.io" not in data["body"] and "> has quit" not in data["body"] and "> has joined #" not in data["body"] and "> has left #" not in data["body"]):
			arr_id.append(data["id"])
			arr_grimoire_creation_date.append(data["grimoire_creation_date"])
			arr_context.append(data["context"])
			arr_body.append(data["body"])
			arr_channel.append(data["data_source"])

	df=pd.DataFrame({
		'id':arr_id,
		'grimoire_creation_date':arr_grimoire_creation_date,
		'context':arr_context,
		'body':arr_body,
		'channel':arr_channel
		})

	convert_csv(df)
	convert_xlsx(df)
	#convert_airtable(df)
	CSV2GSheets()
	
def convert_csv(df):
	df.to_csv(csv_file_name,index=None)
def convert_xlsx(df):
	df.to_excel(xls_file_name, index=None)
def convert_airtable(df):

	post_url = 'https://api.airtable.com/v0/appPmJ0Mbq7tz5yHP/Table2'
	post_headers = {
	    'Authorization' : 'Bearer keylwWqsUb27EACcv',
	    'Content-Type': 'application/json'
	}
	for ind in df.index: 
		id_index=df['id'][ind]
		grimoire_creation_date=df['grimoire_creation_date'][ind]
		context=df['context'][ind]
		body=df['body'][ind]
		channel=df['channel'][ind]	

		data = {
			"fields": {
				"id":id_index,
				"grimoire_creation_date":grimoire_creation_date,
				"context":context,
				"body":body,
				"channel":channel
		        }
		    }

		post_airtable_request = requests.post(post_url, headers = post_headers, json = data)
		print(post_airtable_request.status_code)
	if (post_airtable_request.status_code ==200):
		print("Data successfully exported to Airtable " )


def CSV2GSheets():
	"""
	This scipt uploads the CSV data to a Google Sheets "SCMS"

	Input: CSV file : merged_tagged.csv
	Output: GSheets: SCMS 
	Contains all tagged data: IRC+Github+Mbox

	"""
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

	creds = ServiceAccountCredentials.from_json_keyfile_name("SCMS-creds.json", scope)

	client = gspread.authorize(creds)

	spreadsheet = client.open("SCMS")
	worksheet_scms=spreadsheet.get_worksheet(0)
	scms_data = worksheet_scms.get_all_records()
	content = open('merged_tagged.csv', 'r').read().encode("utf-8")
	client.import_csv(spreadsheet.id, content)

def main():
	global csv_file_name,xls_file_name 
	filename="merged_output"
	csv_file_name= filename+".csv"
	xls_file_name= filename+".xlsx"
	search()
	print("Output files are %s and %s" %(csv_file_name,xls_file_name))

if __name__ == "__main__":
    main()