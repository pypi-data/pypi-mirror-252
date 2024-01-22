import numpy as np
import pandas as pd
import rioxarray as rio
from osgeo import gdal
import geopandas as gpd
from shapely.geometry import box
import datetime
from   .WaPOR_create_nc import get_shp, get_prod_names, get_template, time_index_from_filenames, init_nc, fill_nc_one_timestep
from .WaPOR_utility_funcs import base_url_v3, available_mapset, get_available_data, get_dekadal_timestep, get_agera5_ET0_PCP, lazy_open, get_clipped_ds

import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'scripts'))

import dask

import time
import warnings
from IPython.display import HTML


def list_v3():
    '''
    A function to list the WaPOR V3 downloadable products and the codes to use for downloading them.
    '''
    base_url = base_url_v3()
    available__mapset = available_mapset(base_url)

    available__mapset = available__mapset.drop(['mapset_link', 'scale'], axis=1)

    available__mapset = available__mapset.rename(columns={'caption': 'Product'})
    available__mapset = available__mapset[['Product'] + [col for col in available__mapset.columns if col != 'Product']]

    available__mapset = available__mapset.rename(columns={'measureUnit': 'Unit'})
    available__mapset = available__mapset[['Product', 'Unit'] + [col for col in available__mapset.columns if col not in ['Product', 'Unit']]]

    available__mapset = available__mapset.rename(columns={'code': 'downloading code'})
    available__mapset = available__mapset[[col for col in available__mapset.columns if col != 'downloading code'] + ['downloading code']]

    final_df_html = available__mapset.to_html()
    
    return HTML(final_df_html)


def download_v3(output_dir, start_date, end_date, AOI,output_format='tif', variables=[], delta_box=0.1):
    '''
    This function downloads WaPOR V3 products for one or multiple specified products
    within a given time period and a defined region based on a shapefile.

    Parameters
    -----------
    output_dir: str
        Path to download the products.
    start_date: str
        The starting date for downloading the products.
    end_date: str
        The ending date for downloading the products.
    AOI: str
        Path to the shapefile of the region of interest.
    output_format: str, optional
        Output format for the downloaded files. Default is '.tif'. 
        To download in NetCDF format, use '.nc'.
    variables: list
        Codes of the products to download.
    delta_box: float, optional
        Buffer the bounding box by 'delta_box'. Default is 0.1.

    Returns
    --------
    Downloaded files in either .tif or .nc format for the specified product/s.
    '''

    
    base_url = base_url_v3()
    available__mapset = available_mapset(base_url)
    Availabe_data_list = get_available_data(available__mapset)
    
    
    warnings.simplefilter(action='ignore', category=FutureWarning)
    tt = time.time()

    # WaPOR v3 avaialble period
    per_start = datetime.datetime(2018, 1, 1).strftime("%Y-%m-%d")
    per_end = datetime.datetime.fromisoformat(Availabe_data_list.iloc[-1].endDate)
    WaPOR_v3_period = f"{per_start},{per_end}"

    #Create directories
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # get dates
    Startdate = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    Enddate = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    time_range = f"{Startdate},{Enddate}"

    years = pd.date_range(Startdate, Enddate, freq='AS')
    months = pd.date_range(Startdate, Enddate, freq='MS')
    dekads = get_dekadal_timestep(Startdate, Enddate)

    years = [pd.to_datetime(x).strftime('%Y') for x in years]
    years = [np.datetime64(y) for y in years]

    months = [pd.to_datetime(x).strftime('%Y-%m') for x in months]
    months = [np.datetime64(y) for y in months]

    dekads = [pd.to_datetime(x).strftime('%Y-%m-%d') for x in dekads]
    dekads = [np.datetime64(y) for y in dekads]

    # frequency sysmbols
    sym_freq = {
                'dekadal':'D',
                'monthly':'M',
                'yearly': 'A'
            }

    #  Read the shapefile to get bounding box of for the area of interest
    shape = get_shp(AOI)
    aoi = box(*shape.geometry.total_bounds) # area of interest bounding box polygon

    # buffer the bounding box by 'delta_box'
    buffered_box = aoi.buffer(delta_box)

    # convert the buufered box to geopandas object
    bbox2 = gpd.GeoDataFrame(pd.DataFrame(['p1'], columns = ['geom']),
                crs = 'epsg:4326',
                geometry = [buffered_box])

    xmin,ymin,xmax,ymax = bbox2.geometry.total_bounds

    data2dl = []
    for var in variables:
        level = var.split('-')[0].split('L')[1]
        data2dl.append(var)
        # print(var, level)
        #if (int(level) == 3):
            # code to be chnaged after WaPOR level 3 is out!
            # get the country code
            #df_L3 = catalogue_df[catalogue_df['code'].str.contains("L3")]
            #df_L3_AETI_D = df_L3[df_L3['code'].str.contains("AETI_D")]
            #ccode = get_country_code_for_L3(WaPOR.API, df_L3_AETI_D, WaPOR_v2_period, aoi)
            #if(ccode != -1):
            #    var_name = var.split('_')[0]
            #   prod = 'L'+parser.get(var, 'level')+'_'+ccode+'_'+var_name+'_'+sym_freq[parser.get(var, 'freq').lower()]
            #    data2dl.append(prod)
            #else:
            #    print('AOI is not in the L3 available areas!\n check if you specify the \
            #    corect WaPOR data level for your area of interest.')
            #    sys.exit()
        #else:
        #    data2dl.append(var)
        
    # check if the product to download is in WaPOR products
    WaPOR_products_lst = available__mapset.code.to_list()
    not_WaPOR_prod = [i for i in data2dl if i not in WaPOR_products_lst]
    if not_WaPOR_prod:
        print('{} is not in WaPOR products list. Correct the info in the config file'.format(not_WaPOR_prod))
        
    data2dl_2 = list(set(data2dl) - set(not_WaPOR_prod))

    # Downlaod AETI  raster and clip it so that it can be used as a templat
    temp_file = os.path.join(output_dir, 'template2.tif').replace('\\', '/')

    if not (os.path.exists(temp_file)):
        l3=[x for x in data2dl if 'L3' in x]
        l2=[x for x in data2dl if 'L2' in x]
        l1=[x for x in data2dl if 'L1' in x]
        print(l2)
        if (len(l3)>0):
            rster_2d = l3[0]
        elif (len(l2)>0):
            rster_2d = l2[0]
        else:
            rster_2d = l1[0]

        
        if rster_2d not in WaPOR_products_lst:
            print(f"product: {rster_2d} is not in WaPOR procts list") 
            
            name, frq, level = get_prod_names(rster_2d,sym_freq)
            rster_2d = f"{level}_AETI_{frq}"

        df_aval = Availabe_data_list[Availabe_data_list.code.str.contains(rster_2d)]
        tif_url = df_aval.iloc[0].downloadUrl


        if('L3' in rster_2d):
            ds = gdal.Translate(temp_file, f"/vsicurl/{tif_url}")
        else:
            bands = [1]
            bbox_gdal = [xmin,ymax, xmax,ymin]
            translate_options = gdal.TranslateOptions(projWin=bbox_gdal, bandList=bands, 
                                                    creationOptions = ['TILED=YES', 'COMPRESS=LZW'])
            ds = gdal.Translate(temp_file, f"/vsicurl/{tif_url}", options = translate_options)

    # get template from the saved raster
    template = get_template(temp_file, shape)
    
    #download products which are in WaPOR products list

    for prod in data2dl:
        name, frq, level = get_prod_names(prod,sym_freq)
        print('prod:', prod, 'name:', name)  
        
        # prepare attributes
        if('LCC' in prod):
            no_times = years
            attrs = ({'title': 'Land cover class from WaPOR', 'units': '-', 'period': 'yearly',
                'quantity':name, 'source':'WaPOR'})
        elif(frq == 'monthly'):
            no_times = months
            attrs = ({'title': '{0} from WaPOR'.format(name), 'units': 'mm/month', 'period': 'monthly',
                'quantity':name, 'source':'WaPOR'})
        else:
            no_times = dekads
            attrs = ({'title': '{0} from WaPOR'.format(name), 'units': 'mm/dekad', 'period': 'dekadal',
                'quantity':name, 'source':'WaPOR'})
            
        frqsym = sym_freq[frq]
        
        
        if prod in data2dl_2:
            # extract the conversion factor for the product
            scale_factor = float(available__mapset[available__mapset.code==prod].scale)
            
            # get the urls for the available data
            df_aval = Availabe_data_list[Availabe_data_list.code.str.contains(prod)]
            df_aval_req = df_aval.loc[(df_aval['startDate'] >= f"{ Startdate - datetime.timedelta(days=1)}") &
                                    (df_aval['startDate'] <= f"{Enddate}")]
            urls = df_aval_req.downloadUrl.to_list()
            
            # get time from raster's url
            time_rst = time_index_from_filenames(frq, urls)
            
        if (prod not in data2dl_2) & any(c in prod for c in ('RET', 'PCP')):
            scale_factor = 1
            # get the links from ARGERA5
            #at the moment AGERA5 PCP is available only starting from 2022-04-07
            urls = get_agera5_ET0_PCP(prod, frq, years, months, dekads)
            if frq == 'dekadal':
                time_rst = dekads
            elif frq == 'monthly':
                time_rst = months
            else:
                time_rst = years
        
        if frq == 'dekadal':
            days_idekad = [(x - time_rst[i - 1])/ np.timedelta64(1, 'D') for i, x in enumerate(time_rst) if i > 0]
            days_idekad.append(10)
        
        # get the crs from the first url
        with rio.open_rasterio(urls[0]) as temp:
            crs = temp.rio.crs

        if crs.to_epsg() != 4326:
            # project the bbox for clipping the dataset to the crs of the da
            bbox2.crs = "EPSG:4326" 
            bbox_for_clipping = bbox2#.to_crs({'epsg':crs.to_epsg()})
        else:
            bbox_for_clipping = bbox2

        xmin,ymin,xmax,ymax = bbox_for_clipping.geometry.total_bounds
        
        if output_format == 'tif' :
                #save tif file
            for i, url in enumerate(urls):
                date = time_rst[i]
                date_str = pd.to_datetime(str(date)).strftime('%Y.%m.%d')
                tif_path=os.path.join(output_dir,'W3_'+prod+'_'+date_str+'.tif')
                dataaraay = dask.compute(lazy_open(url))
                da = dataaraay[0].rio.clip_box(minx=xmin, miny=ymin, maxx=xmax, maxy=ymax)
                da = da*scale_factor
                if (frq == 'dekadal') & (prod  in WaPOR_products_lst):
                    da = da*days_idekad[i]
                da.rio.write_crs(crs, inplace=True)
                da.rio.write_nodata(-9999., inplace=True)
                da.rio.to_raster(tif_path, compress= 'LZW', tiled=True, dtype = np.float32)
                
        else:# path of the netCDF file to be created
            nc_path=os.path.join(output_dir,prod+'_W3.nc')
            print("\nwriting the netCDF file {0}".format(nc_path))

            # intailaze the netCDF file
            dims = {'time':  None, 'latitude': None, 'longitude': None}
            dims['longitude'] = template.x.values
            dims['latitude'] = template.y.values
            dim = ('time', 'latitude', 'longitude')
            var = {name:[dim,attrs]}
            init_nc(nc_path, dims, var, fill = np.nan, attr = attrs)
            
            for i, url in enumerate(urls):
                date = time_rst[i]
                da = dask.compute(lazy_open(url))
                da = da[0]
                data = dict()
                if (frq == 'dekadal') & (prod  in WaPOR_products_lst):
                    data[name] = get_clipped_ds(da, prod, shape, xmin, ymin, xmax, ymax, crs, template, scale_factor)*days_idekad[i]
                else:
                    data[name] = get_clipped_ds(da, prod, shape, xmin, ymin, xmax, ymax, crs, template, scale_factor)   
                fill_nc_one_timestep(nc_path, data, date)
                del data


    print("writing completed!")
    elapsed = time.time() - tt
    print(">> Time elapsed up to getting urls : "+"{0:.1f}".format(elapsed)+" s")