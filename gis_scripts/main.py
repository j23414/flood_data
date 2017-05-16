import arcpy
import pandas as pd
from arcpy import env
from arcpy.sa import Raster, Ln, Tan
import math
gis_data_dir = "C:/Users/Jeff/Google Drive/research/Sadler_3rdPaper_GIS_data/"

arcpy.CheckOutExtension("spatial")
env.overwriteOutput = True
env.workspace = gis_data_dir


def calculate_twi():
    slope_raster = Raster("slope_nor.tif")
    flacc = Raster("C:/Users/Jeff/Google Drive/research/Hampton Roads Data/Geographic Data/Raster/"
                   "USGS Nor DEM/mosaic/nor_flacc")
    twi = Ln((flacc+1)/(Tan(slope_raster+.0001)*180./math.pi))
    twi.save('{}twi_arcpy.tif'.format(gis_data_dir))


def calculate_dist_to_water():
    pass


def main():
    calculate_twi()

if __name__ == "__main__":
    main()
