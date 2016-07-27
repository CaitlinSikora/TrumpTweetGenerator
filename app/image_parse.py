from __future__ import division
import json

with open('search.json','r') as f:
  data = f.read()
parsed = json.loads(data)

def grab_widest(parsed):
  max_aspect_ratio = 0
  print parsed['request']
  for item in parsed['items']:
    print item['image']['width'],item['image']['height'],item['image']['width']/item['image']['height']
    print item['link']
    if (item['image']['width']/item['image']['height'])>max_aspect_ratio:
      max_aspect_ratio = item['image']['width']/item['image']['height']
      max_link = item['link']

  return max_link
