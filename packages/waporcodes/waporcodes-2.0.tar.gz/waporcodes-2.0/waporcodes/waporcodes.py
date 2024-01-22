
import requests
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'scripts'))

from IPython.display import HTML
from rich.console import Console
from rich.text import Text

def collect_responses(url, info = ["code"]):
    data = {"links": [{"rel": "next", "href": url}]}
    output = list()
    while "next" in [x["rel"] for x in data["links"]]:
        url_ = [x["href"] for x in data["links"] if x["rel"] == "next"][0]
        response = requests.get(url_)
        response.raise_for_status()
        data = response.json()["response"]
        if isinstance(info, list):
            output += [tuple(x.get(y) for y in info) for x in data["items"]]
        else:
            output += data["items"]
    if isinstance(info, list):
        output = sorted(output)
    return output

def available_mapset(base_url):
    # Available mapsets
    data_lst = collect_responses(base_url, info = ["code", "caption", "measureUnit", "scale", "links"])
    df = pd.DataFrame(data_lst, columns=["code", "caption", "measureUnit", "scale", "links"])
    url_ = [x[0]["href"] for x in df["links"]]
    df['mapset_link'] = url_
    df = df.drop(columns=['links'])
    
    return df


def base_url_v3():
    return  f"https://data.apps.fao.org/gismgr/api/v2/catalog/workspaces/WAPOR-3/mapsets"

def base_url_mosset_v3():
    return f"https://data.apps.fao.org/gismgr/api/v2/catalog/workspaces/WAPOR-3/mosaicsets"

def list_v3():
    '''
    A function to list the WaPOR V3 downloadable products and the codes to use for downloading them.
    '''
    base_url = base_url_v3()
    availablemapset = available_mapset(base_url)

    availablemapset = availablemapset.drop(['mapset_link', 'scale'], axis=1)

    mos_url = base_url_mosset_v3()
    available_mosset = available_mapset(mos_url)
    code_list=[]
    caption_list=[]
    units_list=[]
    for x, y, z in zip (available_mosset['code'], available_mosset['caption'], available_mosset['measureUnit']):
        if x.split('-')[0]=='L3':
            code_list.append(x)
            caption_list.append(y)
            units_list.append(z)
        else:
            continue 

    appended_df = pd.DataFrame({'code': code_list, 'caption': caption_list, 'measureUnit': units_list})
    availablemapset = pd.concat([availablemapset, appended_df], ignore_index=True)

    availablemapset = availablemapset.rename(columns={'caption': 'Product'})
    availablemapset = availablemapset[['Product'] + [col for col in availablemapset.columns if col != 'Product']]

    availablemapset = availablemapset.rename(columns={'measureUnit': 'Unit'})
    availablemapset = availablemapset[['Product', 'Unit'] + [col for col in availablemapset.columns if col not in ['Product', 'Unit']]]

    availablemapset = availablemapset.rename(columns={'code': 'Downloading Code'})
    availablemapset = availablemapset[[col for col in availablemapset.columns if col != 'Downloading Code'] + ['Downloading Code']]

    availablemapset.sort_values(by=['Product', 'Downloading Code'], inplace=True)
    availablemapset = availablemapset.reset_index(drop=True)

    for index, x in zip(availablemapset.index, availablemapset['Downloading Code']):
        if x.split('-')[0] == 'L1':
            availablemapset.loc[index, 'Product'] = availablemapset.loc[index, 'Product'] + ' Level-1'
        elif x.split('-')[0] == 'L2':
            availablemapset.loc[index, 'Product'] = availablemapset.loc[index, 'Product'] + ' Level-2'
        elif x.split('-')[0] == 'L3':
            availablemapset.loc[index, 'Product'] = availablemapset.loc[index, 'Product'] + ' Level-3'

    final_df_html = availablemapset.to_html()

    
    console = Console()
    text = Text('NOTE: Add the country code to the level-3 products for downloading.')
    text.stylize("bold magenta", 0, 6)
    console.print(text)

    ##////////////////////////////////////////////Country codes/////////////////////////////////////////////////////
    
    cubes_request_url = f"https://io.apps.fao.org/gismgr/api/v1/catalog/workspaces/WAPOR_2/cubes?paged=false"
    cubes_request_response = requests.get(cubes_request_url)
    cubes_request_response.raise_for_status()
    df = pd.DataFrame(cubes_request_response.json()["response"])
    filtered_df = df[df['code'].str.contains(r'L3_.*_NPP_D')][['code', 'caption']]
    ccode_list = []
    region_list = []

    for x, y in zip(filtered_df['code'], filtered_df['caption']):
        ccode = x.split('_')[1]
        country = y.split('(')[1].split('-')[0]
        
        ccode_list.append(ccode)
        region_list.append(country)

    filtered_df['Region'] = region_list
    filtered_df['Country_Code'] = ccode_list
    filtered_df = filtered_df.drop(['code','caption'], axis=1)
    filtered_df = filtered_df.reset_index(drop=True)
    final_df_html2 = filtered_df.to_html()
    
    # Concatenate the HTML strings
    final_html = final_df_html + final_df_html2
    
    return HTML(final_html)