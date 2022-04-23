import pickle
import pandas as pd
import os
import cleaning_tools as ct

element_regex ='^[\w]+[,][\s][A-Z][a-z]?([\s][(].+[)])?$'
properties = ['Name', 'URL', 'Density', 'Tensile Strength, Ultimate', 'Tensile Strength, Yield', 'Elongation at Break']

if __name__ == '__main__':
    files = os.listdir('data')
    data = []
    for file in files:
        data.extend(pickle.load(open(os.path.join('data', file), 'rb')))
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
    stage_3 = stage_2[properties + components].reset_index()
    stage_3[components] = stage_3[components].applymap(ct.clean_components)
    print(len(data))