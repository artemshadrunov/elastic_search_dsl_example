from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import collections

es = Elasticsearch('http://34.73.134.19:9200')
indices = [index for index in es.indices.get_alias("*") if 't3.server.event' in index]
supports = []
i = 0
for idx in indices:
    search = Search(using=es, index=idx)
    search = search.source('data.support').params(request_timeout=2000).query("match", **{'data.event':'Excavations'}).filter('range', **{'@timestamp':{'gte': "2019-07-11T10:00:00"}})
    results_raw = search.scan()
    results = [res for res in results_raw]
    supports.extend([res.data.support for res in results])
    i += 1
    print(i)
    
unique_supports = [item for item, count in collections.Counter(supports).items() if count == 1]

print(unique_supports.count)
with open('your_file.txt', 'w') as f:
    for item in unique_supports:
        f.write("%s\n" % item)
print(1)