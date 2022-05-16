import pickle
import pandas as pd
import os
import cleaning_tools as ct
import regex as re
import matminer_test as mmt

element_regex ='^[\w]+[,][\s][A-Z][a-z]?([\s][(].+[)])?$'
identity = ['Name', 'URL']
properties = ['Density', 'Tensile Strength, Ultimate', 'Tensile Strength, Yield', 'Elongation at Break']

def load_scraped_data(directory):
    files = os.listdir(directory)
    data = []
    for file in files:
        data.extend(pickle.load(open(os.path.join(directory, file), 'rb')))
    # Load the list of materials into one big dataframe
    for i, df in enumerate(data):
        if "Component Elements Properties" in df.index:
            data[i] = df[df.index.notnull()].T
        else:
            data[i] = pd.DataFrame()

    stage_1 = pd.concat(data, ignore_index=True)
    # Pick out the "metric" valued rows
    stage_2 = stage_1.loc[stage_1["Component Elements Properties"] == "Metric"]
    # Pick out the columns that we care about
    components = list(stage_2.filter(regex=element_regex, axis='columns').columns)
    stage_3 = stage_2[identity + properties + components].reset_index(drop=True)
    stage_3[components] = stage_3[components].applymap(ct.clean_components)
    stage_3[properties] = stage_3[properties].applymap(ct.clean_properties)
    stage_3 = stage_3.rename(columns=lambda x: re.sub('^\w+,\s', '', x))
    stage_3 = stage_3.rename(columns=lambda x: re.sub('\s\(.+\)$', '', x))
    return stage_3

if __name__ == '__main__':
    
    final_df = pd.DataFrame()
    
    datum1 = load_scraped_data('data')
    datum2 = mmt.load_matmine_data('ni_superalloys_3.json')
    
    final_df = pd.concat([datum1, datum2], ignore_index=True)
    final_df.to_csv('final_test.csv')
    print(final_df.head())
    