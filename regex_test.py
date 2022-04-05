import re

test_string = ['Unobtanium, Xo', 'Crumpets', 'Unobtanium, Xomp', 'Crumpets, Po','Unobtanium, xo']

p = re.compile('^[\w]+[,][\s][A-Z][a-z]$')

print(p)