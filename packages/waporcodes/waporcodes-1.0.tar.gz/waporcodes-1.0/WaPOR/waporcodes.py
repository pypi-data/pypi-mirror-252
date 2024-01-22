
import requests
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'scripts'))
import WaPOR_utility_funcs as wuf

from IPython.display import HTML
from rich.console import Console
from rich.text import Text

def list_v3():
    '''
    A function to list the WaPOR V3 downloadable products and the codes to use for downloading them.
    '''
    base_url = wuf.base_url_v3()
    available_mapset = wuf.available_mapset(base_url)

    available_mapset = available_mapset.drop(['mapset_link', 'scale'], axis=1)

    mos_url = wuf.base_url_mosset_v3()
    available_mosset = wuf.available_mapset(mos_url)
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
    available_mapset = pd.concat([available_mapset, appended_df], ignore_index=True)

    available_mapset = available_mapset.rename(columns={'caption': 'Product'})
    available_mapset = available_mapset[['Product'] + [col for col in available_mapset.columns if col != 'Product']]

    available_mapset = available_mapset.rename(columns={'measureUnit': 'Unit'})
    available_mapset = available_mapset[['Product', 'Unit'] + [col for col in available_mapset.columns if col not in ['Product', 'Unit']]]

    available_mapset = available_mapset.rename(columns={'code': 'Downloading Code'})
    available_mapset = available_mapset[[col for col in available_mapset.columns if col != 'Downloading Code'] + ['Downloading Code']]

    available_mapset.sort_values(by=['Product', 'Downloading Code'], inplace=True)
    available_mapset = available_mapset.reset_index(drop=True)

    for index, x in zip(available_mapset.index, available_mapset['Downloading Code']):
        if x.split('-')[0] == 'L1':
            available_mapset.loc[index, 'Product'] = available_mapset.loc[index, 'Product'] + ' Level-1'
        elif x.split('-')[0] == 'L2':
            available_mapset.loc[index, 'Product'] = available_mapset.loc[index, 'Product'] + ' Level-2'
        elif x.split('-')[0] == 'L3':
            available_mapset.loc[index, 'Product'] = available_mapset.loc[index, 'Product'] + ' Level-3'

    final_df_html = available_mapset.to_html()

    
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