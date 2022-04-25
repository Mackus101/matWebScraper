import pandas as pd
import regex as re
import statistics as stat
import math

comp_tests = ['2.8 - 3.3 %', '62%', '<= 0.020 %', '0.010 - 0.02 %', 'Hi there']
prop_tests = ['1269 MPa@Strain 0.200 %',
              '>= 5.0 %',
              '331 MPa@Diameter 9.70 mm',
              'Temperature 25.0 Â°C',
              '262 MPa',
              '42%',
              '59.0 - 2000 MPa',
              '0.500 - 74.0 %',
              'hello there']

def clean_components(percentage):
    nums = re.findall("\d+[.]?\d*", str(percentage))
    try:
        cleaned_num = stat.mean(list(map(float, nums)))
    except:
        if not(math.isnan(percentage)):
            print("Error with: ", percentage)
        cleaned_num = 0.0
    return cleaned_num

def clean_properties(entry):
    nums = re.findall("(\d+[.]?\d*)(?<!.+[@].+)", str(entry))
    try:
        cleaned_num = stat.mean(list(map(float, nums)))
    except:
        cleaned_num = math.nan
    return cleaned_num

if __name__ == '__main__':
    for test in prop_tests:
        print(clean_properties(test))
        
    print("done")