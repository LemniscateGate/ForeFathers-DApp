import json 
f = open('knowledge/brain.json', encoding='utf-8', errors='ignore') 
data = json.load(f) 
print(type(data), len(data)) 
