# requirements
import pandas as pd
import requests
from io import StringIO
import json


# Display the available datasets
def available_datasets(output='normal'):
    return pd.read_csv('https://raw.githubusercontent.com/Hezel2000/mag4datasets/main/overview_available_datasets.csv')

    # This searches through all json files in the metadata folder 'manually'
    # url = f'https://api.github.com/repos/Hezel2000/mag4datasets/contents/metadata'
    # response = requests.get(url)
    
    # if response.status_code == 200:
    #     files = [file for file in response.json() if file['name'].endswith('.json')]
        
    #     # Fetch and store the contents of each JSON file
    #     json_data = {}
    #     for file in files:
    #         file_url = file['download_url']
    #         file_content_response = requests.get(file_url)
    #         file_content = file_content_response.json()
    #         json_data[file['name']] = file_content
    # else:
    #     return f"Error: Unable to fetch files. Status code: {response.status_code}"

    # if output=='normal':
    #     eList = ['Title', 'Short Title', 'Type', 'Licence', 'Name']

    #     res = []
    #     for i in json_data:
    #         e = json_data[i]
    #         res2 = []
    #         for ei in eList:
    #             res2.append(e[ei])
    #         res.append(res2)

    #     return pd.DataFrame(res, columns=eList)
    # elif output=='full':
    #     return pd.DataFrame(data).T


# Get a specific database
def get_data(dataset_name, property=None, type=None):
    base_url = 'https://raw.githubusercontent.com/Hezel2000/mag4datasets/main/'
    # The file name here does not allow spaces or other characters
    df_dataset_overview = pd.read_csv(base_url + 'overview_available_datasets.csv', on_bad_lines='skip')
    fil = (df_dataset_overview['Title'] == dataset_name) | (df_dataset_overview['Short Title'] == dataset_name)
    db_name = df_dataset_overview[fil]['Title'].values[0]

    if property is None:
        # In the following requests is used, as this allows for spaces or other characters in the file name   
        if type is None or type == 'dataframe':
            csv_url = base_url + 'data/' + db_name + '.csv'
            resp = requests.get(csv_url)
            if resp.status_code == 200:
                return pd.read_csv(StringIO(resp.text))
            else:
                return print('404 – Download failed' +db_name)
        elif type == 'json':
            return print('to be implemented')
        else:
            return print('type not available')
    elif property is not None:
        json_url = base_url + 'json/' + db_name + '.json'
        resp = requests.get(json_url)
        metadata = json.loads(resp.text)
        if property == 'properties':
            return list(metadata.keys())[:-1]
        # the following property can be combined with the 'type' attribute
        elif property == 'all metadata':
            all_metadata = {key: value for key, value in list(metadata.items())[:-1]}
            if type is None or type == 'dataframe':
                df_all_metadata = pd.DataFrame(list(all_metadata.items()), columns=['Key', 'Value'])
                return df_all_metadata
            elif type == 'json':
                return all_metadata
            else:
                return print('type not available')
        else:
            json_url = base_url + 'json/' + db_name + '.json'
            resp = requests.get(json_url)
            metadata = json.loads(resp.text)
            return metadata[property]



#----------- Retired
        
# Likely no longer needed, as all metadata are uploaded alongside the dataset file on the respective mag4 webpage
# # Convert a csv into a json file with metadata
# def write_json_file(file_name, file_path=None, description=None, references=None, source=None, license=None):
#     dataset = pd.read_csv(file_path + '/' + file_name + '.csv').dropna().to_dict()

#     json_file = {
#         "description": description,
#         "references": references,
#         "dois": dois,
#         "source": source,
#         "license": license,
#         "date": date,
#         "version": version,
#         "comment": comment
#     }

#     if file_path is not None:
#         with open(file_path + '/' + file_name + ".json", "w") as outfile:
#             json.dump(json_file, outfile)
#     else:
#         with open(os.getcwd() + '/' + file_name + ".json", "w") as outfile:
#             json.dump(json_file, outfile)

