## STEPS

### STEP 1: ES to Google Sheets

1. Clone GrimoireLab ELK repository:

	`clone https://github.com/chaoss/grimoirelab-elk`

2. Set `setup.cfg` as :

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

3. Set `projects.json` as :

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

4. Execute modred as:

	`--enrich --panels --cfg ./setup.cfg --backends scmssupybot scmsgithub scmspipermail`

5. Set alias :
	
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

6. Write a script `ES2Excel` which will convert Elastic Search index(`all_scms`) into an Excel sheet.

7. Convert the Excel sheet into Google Sheets using GoogleSheets API.

### STEP 2: Google Sheet to Dashboard

1. Import the Google Sheet into a CSV(.csv) or Excel file(.xls)

2. Convert the Excel file to a JSON file using a script `Excel2JSON`. The format of the JSON file is:
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

3. Enrich extra data by modifying the `setup.cfg`:

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

5. Now, we proceed to kibana (https://localhost:5601) and make visualisations. These visualisations lead to a dashboard.