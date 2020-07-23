## STEPS

### STEP 1: ES to Google Sheets

1. Set up GrimpoireLab SirModred. ([Getting-Started](https://github.com/chaoss/grimoirelab-sirmordred/blob/master/Getting-Started.md#getting-started-)) 

2. According to the datasources to be analysed, Set `projects.json` and `setup.cfg` as mentioned [here](https://github.com/chaoss/grimoirelab-sirmordred#supported-data-sources-)

	A simple example could be: 
	1. Set `setup.cfg` as:
	
	```
		[scmspipermail]
		raw_index = scmspipermail_chaoss_raw
		enriched_index = scmspipermail_chaoss_enriched
		no-ssl-verify = true

		[scmsgithub]
		raw_index = scmsgithub_chaoss_raw
		enriched_index = scmsgithub_chaoss_enriched
		api-token = xxxx
		sleep-for-rate = true
		no-archive = true
		category = issue
		sleep-time = 300

		[scmssupybot]
		raw_index = scmssupybot_chaoss_raw
		enriched_index = scmssupybot_chaoss_enriched
	```

	

	2. Set `projects.json` as :

	```
	{
		"chaoss": {
			"scmsgithub": [
				"https://github.com/chaoss/grimoirelab-perceval",
				"https://github.com/chaoss/grimoirelab-elk"
				],
			"scmspipermail": [
				"https://lists.linuxfoundation.org/pipermail/grimoirelab-discussions/"
				],
			"scmssupybot": [
				"irc://chat.freenode.net/chaoss-community /irclogs/freenode/#chaoss-community",
				"irc://chat.freenode.net/grimoirelab /irclogs/freenode/#grimoirelab"
				]
			}
	}
	```

3. Enrich raw data by executing modred with the parameters as:

	`--enrich --panels --cfg ./setup.cfg --backends scmssupybot scmsgithub scmspipermail`

	(Here, add as many data sources you are using in SCMS)

4. Set alias:
	This step is important because we want to refer all (more than 1) SCMS indexes together. Here, in the example below, we have set alias as `all_scms` for 3 SCMS enriched indexes (`scmspipermail_chaoss_enriched`,`scmsgithub_chaoss_enriched`, `scmssupybot_chaoss_enriched`)

	```
	POST /_aliases
	{
	    "actions" : [
	        { "add" : { "index" : "scmspipermail_chaoss_enriched", "alias" : "all_scms" } },
	        { "add" : { "index" : "scmsgithub_chaoss_enriched", "alias" : "all_scms" } },
	        { "add" : { "index" : "scmssupybot_chaoss_enriched", "alias" : "all_scms" } }
	    ]
	}
	```

6. Execute a script `ES2Excel` which will convert Elastic Search index(`all_scms`) into an Excel sheet.
	`python3 utils/ES2Excel.py`

7. Convert the Excel sheet into Google Sheets using GoogleSheets API. For this, set up the `SCMS-creds.json` file present in utils directory. 

### STEP 2: Tagging:

1. Tag all records of the spreadsheet by adding 'scms_tag', 'category','weight'.

2. The possible scms tags are: `Transparency`, `Utility`, `Consistency`, `Merit`, `Trust`.

3. The possible categories depends from 1 community to the other. 

4. Weight is considered from `-3` to `+3`, where a higher weight indicates a more relevant comment/discussion.

### STEP 3: Google Sheet to Dashboard

1. Import the Google Sheet into a CSV(.csv) or Excel file(.xls)

2. Convert the Excel file to a JSON file using a script `Excel2Dashboard`. 

		`python3 utils/Excel2Dashbaord.py`

	The format of the JSON file is:
	```
	[
	    {
	        "conditions": [
	            {
	                "field": "id",
	                "value": "123456789"
	            }
	        ],
	        "set_extra_fields": [
	            {
	                "field": "scms_tags",
	                "value": [
	                    "trust",
	                    "Consistency"
	                ]
	            }
	        ]
	    },
	    {
	        "conditions": [
	            {
	                "field": "id",
	                "value": "123456789"
	            }
	        ],
	        "set_extra_fields": [
	            {
	                "field": "Weight",
	                "value": 0
	            }
	        ]
	    },
	    {
	        "conditions": [
	            {
	                "field": "id",
	                "value": "123456789"
	            }
	        ],
	        "set_extra_fields": [
	            {
	                "field": "Category",
	                "value": "Transactional"
	            }
	        ]
	    }
	]
	```

3. Now, we need to execute a study `enrich_extra_data` to include the tagged information back to the Enriched index. The definition of this study can be found [here](https://github.com/chaoss/grimoirelab-elk/blob/master/grimoire_elk/enriched/enrich.py#L1066).
Enrich extra data by modifying the `setup.cfg` as below.

	```
	[scmspipermail]
	raw_index = scmspipermail_chaoss_raw
	enriched_index = scmspipermail_chaoss_enriched
	no-ssl-verify = true
	studies = [enrich_extra_data:scms]

	[scmsgithub]
	raw_index = scmsgithub_chaoss_raw
	enriched_index = scmsgithub_chaoss_enriched
	api-token = xxxx
	sleep-for-rate = true
	no-archive = true
	category = issue
	sleep-time = 300
	studies = [enrich_extra_data:scms]

	[scmssupybot]
	raw_index = scmssupybot_chaoss_raw
	enriched_index = scmssupybot_chaoss_enriched
	studies = [enrich_extra_data:scms]

	[enrich_extra_data:scms]
	json_url=https://gist.githubusercontent.com/ria18405/630346bac7856658fd19ed63bce4d9c0/raw/61d3afc8aab75219f8ab67218ec377a641cd664b/try.json
	```

4. Execute modred the same way as done above.

5. Click on 'SCMS' on the top menu icon, and enjoy the dashboard 
	![Image description](assets/dash1.png)
	![Image description](assets/dash2.png)

