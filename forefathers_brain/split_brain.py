import json 
f = open('knowledge/brain.json', encoding='utf-8', errors='ignore') 
data = json.load(f) 
chunk_size = 500 
for i in range(0, len(data), chunk_size): 
    chunk = data[i:i+chunk_size] 
    out = open(f'knowledge/brain_{i//chunk_size}.json', 'w', encoding='utf-8') 
    json.dump(chunk, out, ensure_ascii=False) 
    out.close() 
print('Done') 
