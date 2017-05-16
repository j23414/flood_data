import arcpy
import json
import shapefile
import pandas as pd
from arcpy import env
from arcpy.sa import Raster, Ln, Tan, RemapValue, Reclassify, PathDistance
import math
gis_data_dir = "C:/Users/Jeff/Google Drive/research/Sadler_3rdPaper_GIS_data/"

arcpy.CheckOutExtension("spatial")
env.overwriteOutput = True
env.workspace = gis_data_dir


def calculate_twi():
    slope_raster = Raster("slope_nor.tif")
    flacc = Raster("C:/Users/Jeff/Google Drive/research/Hampton Roads Data/Geographic Data/Raster/"
                   "USGS Nor DEM/mosaic/nor_flacc")
    twi = Ln((flacc+1.)/(Tan((slope_raster+.0001)*math.pi/180.)))
    out_file_name = 'twi.tif'
    twi.save(out_file_name)


def reclassify_lulc_for_water():
    lulc_rast = Raster('nor_lulc_ext_prj.tif')
    remap = RemapValue([["11", 1],
                        ["91", 1]
                        ])
    reclass_field = "VALUE"
    water_rast = Reclassify(lulc_rast, reclass_field, remap, "NODATA")
    out_file_name = 'nor_ow_wl.tif'
    water_rast.save(out_file_name)


def calculate_dist_to_water(src_raster):
    """
    uses water raster as source should have run reclassify_lulc_for_water first
    :return: 
    """
    elev_raster = Raster('C:/Users/Jeff/Google Drive/research/Hampton Roads Data/Geographic Data/'
                         'Raster/USGS Nor DEM/mosaic/nor_mosaic.tif')
    path_dist = PathDistance(in_source_data=src_raster, in_surface_raster=elev_raster,
                             in_vertical_raster=elev_raster)
    out_file_name = 'pth_dist_to_wat.tif'
    path_dist.save(out_file_name)


def merge_flood_non_flood():
    flood_pts = 'fld_pts_rd_data.shp'
    non_flood_pts = 'sampled_road_pts.shp'
    out_file_name = 'fld_nfld_pts.shp'
    arcpy.Merge_management([flood_pts, non_flood_pts], out_file_name)


def join_flooded_pts_with_rd_attributes():
    flood_pts = 'flooded_points.shp'
    road_lines = 'nor_roads_centerlines.shp'
    out_file_name = 'fld_pts_rd_data.shp'
    arcpy.SpatialJoin_analysis(flood_pts, road_lines, out_file_name, match_option='CLOSEST')


def join_sw_structures_with_pipe_data():
    data_dir = '{}Stormwater Infrastructure/'.format(gis_data_dir)
    sw_str = '{}Norfolk_SW_Structures.shp'.format(data_dir)
    sw_pipe = '{}Norfolk_SW_Pipes.shp'.format(data_dir)
    out_file_name = '{}sw_structures_joined_pipes.shp'.format(data_dir)
    arcpy.SpatialJoin_analysis(sw_str, sw_pipe, out_file_name, match_option='CLOSEST')
    return out_file_name


def read_shapefile_attribute_table(sf_name):
    sf = shapefile.Reader(sf_name)
    records = sf.records()
    df = pd.DataFrame(records)
    sf_field_names = [i[0] for i in sf.fields]
    df.columns = sf_field_names[1:]
    df.reset_index(inplace=True)
    return df


def sample_road_points():
    fld_pts = '{}fld_pts_rd_data.shp'.format(gis_data_dir)
    rd_pts = '{}road_points.shp'.format(gis_data_dir)
    fld_pt_df = read_shapefile_attribute_table(fld_pts)
    rd_pts_df = read_shapefile_attribute_table(rd_pts)
    cls = fld_pt_df.groupby('VDOT')['count'].sum().sort_values(ascending=False)
    cls = cls / cls.sum() * 100
    print cls
    num_samples = (cls * 800 / 100).round()

    l = []
    for c, n in num_samples.iteritems():
        d = rd_pts_df[rd_pts_df['VDOT'] == c]
        idx = d.sample(n=int(n)).index
        l.append(pd.Series(idx))
    sampled = pd.concat(l)
    out_file_name = 'sampled_road_pts.shp'
    where_clause = '"FID" IN ({})'.format(",".join(map(str, sampled.tolist())))
    arcpy.Select_analysis(rd_pts, out_file_name, where_clause)
    return sampled


def make_basin_shapefile():
    sw_strct = '{}/Stormwater Infrastructure/sw_structures_joined_pipes.shp'.format(gis_data_dir)
    basin_codes = filter_sw_struc_codes('basin')
    where_clause = '"Structure1" IN (\'{}\')'.format("','".join(map(str, basin_codes)))
    out_file_name = '{}/Stormwater Infrastructure/sw_struct_basins.shp'.format(gis_data_dir)
    arcpy.Select_analysis(sw_strct, out_file_name, where_clause)
    return out_file_name


def filter_sw_struc_codes(term='basin'):
    metadata_file_name = '{}/Stormwater Infrastructure/nor_sw_structures_metadata.txt'.format(
        gis_data_dir)
    with open(metadata_file_name) as sw_data:
        d = json.load(sw_data)
    structure_types = d['fields'][3]['domain']['codedValues']
    basin_codes = []
    for s in structure_types:
        if term in s['name'].lower():
            basin_codes.append(s['code'])
    return basin_codes


def main():
    make_basin_shapefile()

if __name__ == "__main__":
    main()
