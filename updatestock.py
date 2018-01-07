import json





filename = "stock.json"

#Read JSON data into the datastore variable
if filename:
    with open(filename, 'r') as f:
        datastore = json.load(f)


print(datastore)

count = 0;
for item in datastore:
	item['pk'] = count
	count+=1;


writefile = "stock_updated.json"
if writefile:
    # Writing JSON data
    with open(writefile, 'w') as f:
        json.dump(datastore, f)