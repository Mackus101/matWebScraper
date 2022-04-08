import re

test_string = ['Unobtanium, Xo', 'Crumpets', 'Unobtanium, Xomp', 'Crumpets, Po','Unobtanium, X', 'Unobtanium, X (Poggers)']

p = re.compile('^[\w]+[,][\s][\w]*')

print(p)