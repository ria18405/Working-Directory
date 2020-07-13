import pandas as pd 
import random
df=pd.read_csv("merged_output.csv")
tags=["trust","transperency","utility","merit","Consistency",
		"trust,transperency","trust,utility","trust,merit","trust,Consistency",
		"transperency,utility","transperency,merit","transperency,Consistency",
		"utility,merit","utility,Consistency","merit,Consistency",
		"trust,transperency,utility","trust,transperency,merit","trust,transperency,Consistency",
		"trust,utility,merit","trust,utility,Consistency","trust,merit,Consistency",
		"transperency,utility,merit","transperency,utility,Consistency","transperency,merit,Consistency","utility,merit,Consistency", 
		"trust,transperency,utility,merit","trust,transperency,utility,Consistency",
		"trust,transperency,merit,Consistency","trust,utility,merit,Consistency","transperency,utility,merit,Consistency"
		]
categories=["Support Response","Incoming Request","Interpersonal","Operational","Transactional"]

for i in range(len(df)):
	random_tag=random.randint(0,len(tags)-1)
	random_wt=random.randint(-3,3)
	random_category=random.randint(0,len(categories)-1)
	# df.loc[i,'scms_tag']=tags[random_tag].split(',')
	df.set_value(i, 'scms_tag', str(tags[random_tag].split(',')))
	df.set_value(i,'Weight',random_wt)
	df.set_value(i,'Category',categories[random_category])

df.to_csv("tagged_output.csv",index=None)
df.to_excel("tagged_output.xlsx",index=None)
