import re

with open('/root/test', 'r') as opened:
    hosts = opened.read()

re.sub('nomemacchina', 'nuovonm', hosts)

with open('/root/test', 'w')
