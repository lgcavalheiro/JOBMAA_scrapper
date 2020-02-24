import sys

import requests
from lxml.etree import HTML

print(sys.version)
print(sys.executable)

r = requests.get('https://google.com')
print(r.status_code)
root = HTML(r.content)
test = root.xpath('//a/@alt="last pagee"')
