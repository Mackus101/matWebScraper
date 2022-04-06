import re

test_string = ['Unobtanium, Xo', 'Crumpets', 'Unobtanium, Xomp', 'Crumpets, Po','Unobtanium, X']

p = re.compile('^[\w]+[,][\s][A-Z][a-z]{0,1}$')

print(p)