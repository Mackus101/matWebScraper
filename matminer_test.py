import pandas as pd
from matminer.data_retrieval.retrieve_Citrine import CitrineDataRetrieval
from matminer.featurizers.composition import alloy
import json

# cdr = CitrineDataRetrieval(api_key="8krqnLRLrTzvlPXSH8w9QQtt")

# df = cdr.get_dataframe(criteria={"data_set_id":153493}, 
#                        properties=["Yield Strength", "Ultimate Tensile Strength"],
#                        secondary_fields=True)

search_terms = ['Yield Strength', 'Ultimate Tensile Strength', 'Elongation']
compat_rename = {'Ultimate Tensile Strength':'Tensile Strength, Ultimate',
                 'Yield Strength':'Tensile Strength, Yield',
                 'Elongation':'Elongation at Break',
                 'names':'Name'}

def format_entry(entry):
    elements = pd.json_normalize(entry['composition']).set_index('element').T
    name = pd.DataFrame({"names" : [entry["names"][0]]})
    properties = pd.json_normalize(entry["properties"]).set_index("name") ## This might be better done with a for loop and if statements
    properties = properties[:][properties.index.isin(search_terms)]
    properties = properties["scalars"].apply(lambda x: x[0]["value"])
    
    formed_entry = pd.concat([name, pd.DataFrame(properties).T.reset_index(drop=True), elements.reset_index(drop=True)], axis='columns')

    return formed_entry

def format_superalloys(data):
    formatted_data = pd.DataFrame()
    for entry in data:
        format_entry(entry)
        formatted_data = pd.concat([formatted_data, format_entry(entry)], ignore_index=True)
        
    formatted_data = formatted_data.rename(columns=compat_rename)
    return formatted_data

def load_matmine_data(filepath):
    
    with open('ni_superalloys_3.json','r') as f:
        data = json.loads(f.read())
    
    return format_superalloys(data)

if __name__ == "__main__":
    
    test = load_matmine_data('ni_superalloys_3.json')

    print(test.head())