import numpy as np
import pandas as pd
import rioxarray as rio
import geopandas as gpd
import netCDF4
import datetime
import calendar
import shutil
import rasterio
import os
 #functions to search and parse dates from file names (for create_netCDF files
import re
def get_date(s_date):
    date_patterns = [ "%Y-%m-%d", "%Y.%m.%d","%Y-%m","%Y.%m","%d-%m-%Y", "%d.%m.%Y","%Y/%m/%d", "%y", 
                     "%y%m","%Y", "%y%m%d"]
    
    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(s_date, pattern).date()
        # datetime.datetime.strptime(s_date,'%y').strftime('%Y')
        except:
            pass
        
def search_date(filename):
    patterns = ['\d{4}.\d{2}.\d{2}','\d{4}.\d{2}', '\d{4}$','\d{4}', '\d{2}$',
                '\d{4}-\d{2}-\d{2}','\d{4}-\d{2}']
    for pattern in patterns:
            try:
                match = re.search(pattern, filename)
                if match:
                    return match
            except:
                pass    
def dekadal2datetime(d):
   
    dknum = int(str(d)[-2:])
    mn = dknum // 3 + (dknum % 3 > 0)
    if(dknum % 3 > 0):
        dkcls = dknum % 3
    else:
        dkcls = 3
    
    yr = int('20'+(str(d)[-4:-2]))
   
    if dkcls == 1:
        day = '0'+str(1)
    elif dkcls == 2:
        day = 11
    elif dkcls == 3:
        day = 21
        # day = calendar.monthrange(yr, mn)[1]
    dstr = '{0}-{1}-{2}'.format(yr, mn, day)
    return dstr

def dekadal2datetime_v3(d):
    yr = int(str(d)[0:4])
    mn = int(str(d)[5:7])
    if(str(d)[-2:] == 'D1'):
        day = '0'+str(1)
    elif(str(d)[-2:] == 'D2'):
        day = 11
    else:
        day = 21
        # day = calendar.monthrange(yr, mn)[1]

    dstr = '{0}-{1}-{2}'.format(yr, mn, day)
    return dstr
    
def time_index_from_filenames(step, fh):
    
    '''helper function to create a pandas DatetimeIndex
       Filename example: xxx_2015.05.20.tif'''    
    filenames = [os.path.splitext(f)[0] for f in fh]
    # print([search_date(f[-10:]) for f in filenames])
    if (step == 'dekadal') and ('WAPOR-3' in filenames[0]):
        d = [get_date(dekadal2datetime_v3(f[-10:])) for f in filenames]
    elif (step == 'dekadal'):
        d = [get_date(dekadal2datetime((search_date(f[-10:]).group()))) for f in filenames]
    else:
        d = [get_date((search_date(f[-10:]).group())) for f in filenames]
    
    dd = [np.datetime64(i) for i in d] 
    # print(dd)
    return dd


def get_shp(fh):
    shape = gpd.read_file(fh)
    # project if the shapefile is not in wsg64
    epsg_code = shape.crs.to_epsg()
    if(epsg_code != 4326): #|(shape.crs != "EPSG:4326")):
        shape = shape.to_crs("epsg:4326")
    return shape
def get_prod_names(prod, sym_freq):
    if('_' in prod):
        split_str = '_'
    else:
        split_str = '-'
    
    prod_split = prod.split(split_str)
    name = prod_split[-2]
    frq = list(sym_freq.keys())[list(sym_freq.values()).index(prod_split[-1])]
    level = int(prod_split[0][1:])
    return name, frq, level

def delet_dir2(folder):
    try:
        shutil.rmtree(folder)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (folder, e))
            
def delet_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def get_template(temp_file, shape):
    # Use rioxarray to open the raster file
    temp = rio.open_rasterio(temp_file, masked=True)
    temp.rio.write_crs("EPSG:4326", inplace=True)

    # Clip to the shape geometry
    temp = temp.rio.clip(shape.geometry.values, shape.crs, drop=True)

    # If the order of y-coordinates is inverted, reverse it
    if temp.y[-1] < temp.y[0]:
        temp = temp.reindex(y=temp.y[::-1])

    # Ensure the CRS is set to EPSG:4326
    #Stemp = temp.rio.reproject("EPSG:4326")

    # Extract attributes and update the CRS
    attrs = temp.attrs
    attrs.update({'crs': 'EPSG:4326'})
    temp.attrs = attrs

    return temp

def init_nc(name_nc, dim, var, fill = -9999., attr = None):
    # Create new nc-file. Existing nc-file is overwritten.
    try: name_nc.close()  # just to be safe, make sure dataset is not already open.
    except: pass

    out_nc = netCDF4.Dataset(name_nc, 'w', format='NETCDF4')
    
    # Add dimensions to nc-file.
    for name, values in dim.items():
        # Create limited dimensions.
        if values is not None:
            out_nc.createDimension(name, values.size)
            vals = out_nc.createVariable(name, 'f4', (name,), fill_value = fill)
            vals[:] = values
        # Create unlimited dimensions.
        else:
            out_nc.createDimension(name, None)
            vals = out_nc.createVariable(name, 'f4', (name,), fill_value = fill)
            vals.calendar = 'standard'
            vals.units = 'days since 1970-01-01 00:00'
               
    # Create variables.
    for name, props in var.items():
        vals = out_nc.createVariable(props[1]['quantity'], 'f4', props[0], zlib = True, 
                                      fill_value = fill, complevel = 9, 
                                      least_significant_digit = 1)
        vals.setncatts(props[1])

    if attr != None:
        out_nc.setncatts(attr)
    # Close nc-file.
    out_nc.close()


def fill_nc_one_timestep(nc_file, var, time_val = None):
    # Open existing nc-file.
    out_nc = netCDF4.Dataset(nc_file, 'r+')
    varis = out_nc.variables.keys()
    dimis = out_nc.dimensions.keys()
    
    # Add time-dependent data to nc-file.
    if time_val is not None:
        time = out_nc.variables['time']
        tidx = time.shape
        time[tidx] = time_val
        
        for name in [x for x in varis if "time" in out_nc[x].dimensions and x not in dimis]:
            field = out_nc.variables[name]
            
            if name in var.keys():
                field[tidx,...] = var[name]
                
            else:
                shape = tuple([y for x, y in enumerate(out_nc[name].shape) if out_nc[name].dimensions[x] != "time"])
                dummy_data = np.ones(shape) * out_nc[name]._FillValue
                field[tidx,...] = dummy_data
    
    # Add invariant data to nc-file.
    else:
         for name, data in var.items():
            out_nc.variables[name][0::] = data
            
    # Close nc-file.
    out_nc.close()

# def re_index_with_tolerance(f, chunks, ds_first):
#     with rio.open_rasterio(f, chunks=chunks) as da:
#         ds = da.reindex_like(ds_first, method='nearest', tolerance=1e-7)
#         # _, ds = xr.align(ds_first, ds, join='override') ## This also works but tolerance is not cosidred, Id dims asre the same
#         da.close()
#         del da
#     return ds


