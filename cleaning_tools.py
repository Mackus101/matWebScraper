import pandas as pd
import re
import statistics as stat
import math

tests = ['2.8 - 3.3 %', '62%', '<= 0.020 %', '0.010 - 0.02 %', 'Hi there']

def clean_components(percentage):
    nums = re.findall("\d+[.]?\d*", str(percentage))
    try:
        cleaned_num = stat.mean(list(map(float, nums)))
    except:
        if not(math.isnan(percentage)):
            print("Error with: ", percentage)
        cleaned_num = 0.0
    return cleaned_num

if __name__ == '__main__':
    for test in tests:
        print(clean_components(test))
        
    print("done")