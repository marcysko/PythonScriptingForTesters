import json

json_data = open('jiraJsonData.json').read()
data = json.loads(json_data)