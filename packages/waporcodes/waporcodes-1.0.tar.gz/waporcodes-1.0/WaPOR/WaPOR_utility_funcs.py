import requests
import numpy as np
import pandas as pd
import rioxarray as rio
import geopandas as gpd
import netCDF4
import dask
import datetime
import shutil
import os

from dask.distributed import Client, LocalCluster, progress
import multiprocessing as mp
 #functions to search and parse dates from file names (for create_netCDF files
import re

# start multiprocessing
def start_multiprocessing():
    try:
        client = Client('tcp://localhost:8786', timeout='4s')
        return client
    except OSError:
        cluster =  LocalCluster(ip="",n_workers=int(0.9 * mp.cpu_count()),
            scheduler_port=8786,
            processes=True,
            threads_per_worker=4,
            memory_limit='16GB',
            local_directory='/tmp'
        )
    return Client(cluster)


@dask.delayed
def lazy_open(href):
    chunks=dict(band=1, x = "auto", y = -1)
    # chunks=dict(band=1, x=4000, y=4000)
    return rio.open_rasterio(href, chunks=True).squeeze(dim = 'band', drop = True)

@dask.delayed
def lazy_open_clip(href, xmin, ymin, xmax, ymax):
    # chunks=dict(band=1, x=4000, y=4000)
    # chunks={'time': '500MB'}
    return rio.open_rasterio(href, chunks=True).rio.clip_box(minx=xmin, miny=ymin, maxx=xmax, maxy=ymax)


# get dekadal timesteps 
def get_dekadal_timestep(begin,end):
    dtrange = pd.date_range(begin, end)
    d = dtrange.day - np.clip((dtrange.day-1) // 10, 0, 2)*10 - 1
    date = dtrange.values - np.array(d, dtype="timedelta64[D]")
    return np.unique(date)

# def get_country_code_for_L3_v2(wapor_api, df, period, aoi):
#     for code in df["code"].str.split("_").str[1]:
#         cube_code = f"L3_{code}_AETI_D"
#         df_avail = wapor_api.getAvailData(cube_code = cube_code, time_range=period)
#         lst = df_avail.iloc[0]["bbox"]
#         value_ind = [i for i, d in enumerate(lst) if "value" in d.keys() and "EPSG:4326" in d.values()] # index of the dict where there is a 'value' 
#         bbox = df_avail.iloc[0]["bbox"][value_ind[0]]["value"]
#         geom = box(*bbox)
#         if(geom.contains(aoi)): 
#             print('the AOI is within {0}'.format(code))
#             return code
#             break
#     return -1  #'AOI is not in the L3 available areas'

def get_country_code_for_L3_v2(df_mapset, df, aoi):
    for code in df["code"].str.split("_").str[1]:
        cube_code = f"L3_{code}_AETI_D"
        _,_,df_avail = get_raster_info(df_mapset, cube_code) #wapor_api.getAvailData(cube_code = cube_code, time_range=period)
        bbox = df_avail.iloc[0]["bbox"]
        geom = box(*bbox)
        if(geom.contains(aoi)): 
            print('the AOI is within {0}'.format(code))
            return code
            break
    return -1  #'AOI is not in the L3 available areas'


def get_country_code_for_L3_v3(ccode, pcode, freq, period, aoi):
 
    cube_code = f"L3_{pcode}_{freq}.{ccode}"
    df_avail = wapor_api.getAvailData(cube_code = cube_code, time_range=period) # this needs to be changed to mosaicset/L3-{prod}-{freq}
    lst = df_avail.iloc[0]["bbox"]
    value_ind = [i for i, d in enumerate(lst) if "value" in d.keys() and "EPSG:4326" in d.values()] # index of the dict where there is a 'value' 
    bbox = df_avail.iloc[0]["bbox"][value_ind[0]]["value"]
    geom = box(*bbox)
    if(geom.contains(aoi)): 
        print('the AOI is within {0}'.format(code))
        return code
    
return -1  #'AOI does not match the provided area code

def get_clipped_ds(da, prod, shape, xmin, ymin, xmax, ymax, crs, template, scale_factor):
    if('L3' not in prod):
        # clip by bounding box
        clipped = da.rio.clip_box(minx=xmin, miny=ymin, maxx=xmax, maxy=ymax)
    else:
        clipped = da
    del da
    
    if crs.to_epsg() != 4326:
        clipped = clipped.rio.reproject("EPSG:4326")
        clipped.rio.write_crs("EPSG:4326", inplace=True)
            
    if (clipped.x != template.x).all() or (clipped.y != template.y).all():
        clipped = clipped.interp({'x':template.x, 'y':template.y}, method='nearest')

    clipped = clipped.rio.clip(shape.geometry.values, shape.crs)       
    clipped = clipped.rename( x ='longitude', y = 'latitude')
    
    clipped = clipped.where(clipped !=clipped.attrs['_FillValue'])
    if clipped.latitude[-1] <clipped.latitude[0]:
        clipped=clipped.reindex(latitude=clipped.latitude[::-1])
    
    return clipped*scale_factor

def get_clipped_ds2(da, prod, shape, crs, template, scale_factor):
    # if('L3' not in prod):
    #     # clip by bounding box
    #     clipped = da.rio.clip_box(minx=xmin, miny=ymin, maxx=xmax, maxy=ymax)
    # else:
    #     clipped = da
    # del da
    clipped = da
    if crs.to_epsg() != 4326:
        clipped = da.rio.reproject("EPSG:4326")
        clipped.rio.write_crs("EPSG:4326", inplace=True)
            
    if (clipped.x != template.x).all() or (clipped.y != template.y).all():
        clipped = clipped.interp({'x':template.x, 'y':template.y}, method='nearest')

    clipped = clipped.rio.clip(shape.geometry.values, shape.crs)       
    clipped = clipped.rename( x ='longitude', y = 'latitude')
    
    clipped = clipped.where(clipped !=clipped.attrs['_FillValue'])
    if clipped.latitude[-1] <clipped.latitude[0]:
        clipped=clipped.reindex(latitude=clipped.latitude[::-1])
    
    return clipped*scale_factor

def base_url_v3():
    return  f"https://data.apps.fao.org/gismgr/api/v2/catalog/workspaces/WAPOR-3/mapsets"

def base_url_mosset_v3():
    return f"https://data.apps.fao.org/gismgr/api/v2/catalog/workspaces/WAPOR-3/mosaicsets"

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

def get_available_data(df):
    mapset_dfs = []
    for mapset_code in df.code:
        mapset_url = f"{df.loc[df.code == mapset_code, 'mapset_link'].values[0]}/rasters"
        data_mapset = collect_responses(mapset_url, info = ['code', "dimensions","downloadUrl"])
        df_mapset = pd.DataFrame(data_mapset, columns=['code', "dimensions","downloadUrl"])
        startDate = [x[0]["member"]['startDate'] for x in df_mapset["dimensions"]]
        endDate = [x[0]["member"]['endDate'] for x in df_mapset["dimensions"]]
        df_mapset['startDate'] = startDate
        df_mapset['endDate'] = endDate
        df_mapset = df_mapset.drop(columns=['dimensions'])
        mapset_dfs.append(df_mapset)
    return pd.concat(mapset_dfs, axis = 0)
    # df_available
    
def get_agera5_ET0_PCP(prod, frq, years, months, dekads):
    if frq == 'dekadal':
        dekads = [pd.to_datetime(x) for x in dekads]
        dks = [str(x.year)+ 'D'+str(x.dayofyear//10+1) for x in dekads]
        dks = [x[:5] + '0' + x[5:] if len(x) != 7 else x for x in dks]
        if('RET' in prod):      
            urls = [f"https://data.apps.fao.org/static/data/c3s/AGERA5_ET0_D/AGERA5_ET0_{dk}.tif" for dk in dks]
        elif('PCP' in prod):
            urls = [f"https://data.apps.fao.org/static/data/c3s/AGERA5_PF_D/AGERA5_PF_{dk}.tif" for dk in dks]
        else:
            print(f"{prod} is not either 'RET or PCP")
    elif frq == 'monthly':
        months = [pd.to_datetime(x) for x in months]
        mns = [str(x.year)+ 'M'+str(x.month) for x in months]
        mns = [x[:5] + '0' + x[5:] if len(x) != 7 else x for x in mns]
        if('RET' in prod):      
            urls = [f"https://data.apps.fao.org/static/data/c3s/AGERA5_ET0_M/AGERA5_ET0_{mn}.tif" for mn in mns]
        elif('PCP' in prod):
            urls = [f"https://data.apps.fao.org/static/data/c3s/AGERA5_PF_M/AGERA5_PF_{mn}.tif" for mn in mns]
        else:
            print(f"{prod} is not either 'RET or PCP")
            
    else:
        years = [pd.to_datetime(x) for x in years]
        yrs = [x.year for x in years]
        if('RET' in prod):      
            urls = [f"https://data.apps.fao.org/static/data/c3s/AGERA5_ET0_A/AGERA5_ET0_{yr}.tif" for yr in yrs]
        elif('PCP' in prod):
            urls = [f"https://data.apps.fao.org/static/data/c3s/AGERA5_PF_A/AGERA5_PF_{yr}.tif" for yr in yrs]
        else:
            print(f"{prod} is not either 'RET or PCP")
            
    return urls

def available_mapset_Wapor_v2(api_token):
    api_token = os.environ['WAPOR_API']
    authorization_request_url = "https://io.apps.fao.org/gismgr/api/v1/iam/sign-in"
    authorization_headers = {"X-GISMGR-API-KEY": api_token}
    authorization_request_response = requests.post(authorization_request_url, headers = authorization_headers)
    authorization_request_response.raise_for_status()
    access_token = authorization_request_response.json()["response"]["accessToken"]
    # get available cubes
    cubes_request_url = f"https://io.apps.fao.org/gismgr/api/v1/catalog/workspaces/WAPOR_2/cubes?paged=false"
    cubes_request_response = requests.get(cubes_request_url)
    cubes_request_response.raise_for_status()
    # get mapset code in links
    df_mapset = pd.DataFrame(cubes_request_response.json()["response"])
    url_ = [x[0]["href"] for x in df_mapset["links"]]
    df_mapset['mapset_link'] = url_
    df_mapset = df_mapset.drop(columns=['links','workspaceCode', 'dataType','index'])
    return access_token, df_mapset

def get_raster_info(df_mapset, prod_code):
    code_request_url = df_mapset[df_mapset.code == prod_code].mapset_link.values[0]
    code_request_response = requests.get(code_request_url)
    code_request_response.raise_for_status()
    code_request_response.json()["response"]
    cube_url = code_request_response.json()["response"]['links'][4]['href']
    
    unit = code_request_response.json()["response"]['additionalInfo']['unit']
    conversion_factor = code_request_response.json()["response"]['additionalInfo']['conversionFactor']
    conversion_factor = float(re.findall("\d+\.\d+",conversion_factor)[0])

    if(prod_code[-1] == 'D'):
        df_col = 'DEKAD'
    elif(prod_code[-1] == 'M'):
        df_col = 'MONTH'
    else:
        df_col = 'YEAR'
    data_lst = collect_responses(cube_url, info = ["rasterId", df_col, 'bbox'])
    df = pd.DataFrame(data_lst, columns=["code", df_col, 'bbox'])
    mn = [x["code"] for x in df[df_col]]
    bbox_val = [x[0]["value"] for x in df["bbox"]]
    df[df_col] = mn
    df['bbox'] = bbox_val
    return unit, conversion_factor, df

def get_downlaodurl_Wapor_v2(access_token, prod_code, raster_id_lst):
    workspace = "WAPOR_2"
    downloadurls = []
    tif_headers = {"Authorization": f"Bearer {access_token}"}
    for rsid in raster_id_lst:
        tif_request_url = f"https://io.apps.fao.org/gismgr/api/v1/download/{workspace}?requestType=MAPSET_RASTER&cubeCode={prod_code}&rasterId={rsid}"
        tif_request_response = requests.get(tif_request_url, headers = tif_headers)
        tif_request_response.raise_for_status()
        tif_url = tif_request_response.json()["response"]["downloadUrl"]
        # print(tif_url)
        #write each item on a new line
        downloadurls.append(tif_url)
    return downloadurls