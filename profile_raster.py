import sys, gdal, os
from gdalconst import GA_ReadOnly
from os.path import realpath
from shapely import wkt
from shapely.geometry import LineString
from osgeo import ogr
import pandas as pd
import matplotlib.pyplot as plt
import glob

def make_profile_plot(csv_file, NO_DATA):
    df = pd.read_csv(csv_file)
    filter_df = df[df['elevation']!=NO_DATA]
    x = filter_df['distance']
    z = filter_df['elevation']
    plt.plot(x, z)
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Elevation (m)')
    plt.tight_layout()
    plt.savefig(os.path.splitext(csv_file)[0]+'fig.png', dpi=300)
    plt.close()
def make_profile_plot_mutliple(save_image, out_folder, NO_DATA):
    csvs = glob.glob(out_folder + '\*.csv')
    for csv_file in csvs:
        name = os.path.splitext(os.path.basename(csv_file))[0]
        df = pd.read_csv(csv_file)
        filter_df = df[df['elevation']!=NO_DATA]
        x = filter_df['distance']
        z = filter_df['elevation']
        plt.plot(x, z, label=name)
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Elevation (m)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_image, dpi=300)
    plt.close()


def get_elevation(x_coord, y_coord, raster, bands, gt):
    """
    get the elevation value of each pixel under
    location x, y
    :param x_coord: x coordinate
    :param y_coord: y coordinate
    :param raster: gdal raster open object
    :param bands: number of bands in image
    :param gt: raster limits
    :return: elevation value of raster at point x,y
    """
    elevation = []
    xOrigin = gt[0]
    yOrigin = gt[3]
    pixelWidth = gt[1]
    pixelHeight = gt[5]
    px = int((x_coord - xOrigin) / pixelWidth)
    py = int((y_coord - yOrigin) / pixelHeight)
    for j in range(bands):
        band = raster.GetRasterBand(j + 1)
        data = band.ReadAsArray(px, py, 1, 1)
        elevation.append(data[0][0])
    return elevation


def write_to_csv(csv_out,result_profile_x_z):
    # check if output file exists on disk if yes delete it
    if os.path.isfile(csv_out):
        os.remove(csv_out)
   
    # create new CSV file containing X (distance) and Z value pairs
    with open(csv_out, 'a') as outfile:
        # write first row column names into CSV
        outfile.write("distance,elevation" + "\n")
        # loop through each pair and write to CSV
        for x, z in result_profile_x_z:
            outfile.write(str(round(x, 2)) + ',' + str(round(z, 2)) + '\n')
           

def main(in_raster, in_line, csv_file, res, NO_DATA, batch=False):
    """
    Extracts elevation profile given an input raster dem and an input shapefile line
    inputs:
    in_raster: path to raster dem
    in_line: path to shapefile profile line
    csv_file: path to save extracted distance, elevation pairs to
    res: resolution to sample at in meters
    N0_DATA: raster no data value
    batch (optional): this should stay as False if just one profile is taken, use batch_main function for multiple profiles
    """
    # open the image
    ds = gdal.Open(in_raster, GA_ReadOnly)
   
    if ds is None:
        print('Could not open image')
        sys.exit(1)
   
    # get raster bands
    bands = ds.RasterCount
   
    # get georeference info
    transform = ds.GetGeoTransform()
    if batch == False:
        # line defining the profile
        line_file = ogr.Open(in_line)
        shape = line_file.GetLayer(0)
        #first feature of the shapefile
        line = shape.GetFeature(0)
        line_geom = line.geometry().ExportToWkt()
        shapely_line = LineString(wkt.loads(line_geom))
        # length in meters of profile line
        length_m = shapely_line.length
    else:
        line_geom = in_line.geometry().ExportToWkt()
        shapely_line = LineString(wkt.loads(line_geom))
        # length in meters of profile line
        length_m = shapely_line.length
    # lists of coords and elevations
    x = []
    y = []
    z = []
    # distance of the topographic profile
    distance = []
    for currentdistance in range(0, int(length_m), res):
        # creation of the point on the line
        point = shapely_line.interpolate(currentdistance)
        xp, yp = point.x, point.y
        x.append(xp)
        y.append(yp)
        # extraction of the elevation value from the MNT
        z.append(get_elevation(xp, yp, ds, bands, transform)[0])
        distance.append(currentdistance)  
   
    # combine distance and elevation vales as pairs
    profile_x_z = zip(distance,z)
   
    # output final csv data
    write_to_csv(csv_file, profile_x_z)
    make_profile_plot(csv_file, NO_DATA)

def batch_main(in_raster, in_lines, out_folder, res, NO_DATA):
    """
    Repeatedly take elevation profiles from a raster dem with an input shapefile containing all of the lines
    inputs:
    in_raster: path to raster dem
    in_lines: path to shapefile containing profile lines
    out_folder: path to folder to save csvs and png figures to
    res: resolution to sample at in meters
    NO_DATA: no data value for raster
    """
    line_file = ogr.Open(in_lines)
    layer = line_file.GetLayer(0)
    i=1
    for feature in layer:
        csv_path = os.path.join(out_folder, 'transect'+str(i)+'.csv')
        main(in_raster, feature, csv_path, res, NO_DATA, batch=True)
        i=i+1
        
def main_raster(in_rasters, in_line, save_folder, res, NO_DATA, batch=False):
    """
    Extracts elevation profile given multiple input raster dems and an input shapefile line
    inputs:
    in_raster_folder: list containing paths to raster dems
    in_line: path to shapefile profile line
    csv_folder: path to save results to (csvs, png figure)
    res: resolution to sample at in meters
    N0_DATA: raster no data value
    batch (optional): this should stay as False if just one profile is taken, use batch_main_raster function for multiple profiles
    """
    
    for in_raster in in_rasters:
        print(in_raster)
        name = os.path.splitext(os.path.basename(in_raster))[0]
        # open the image
        ds = gdal.Open(in_raster, GA_ReadOnly)
       
        if ds is None:
            print('Could not open image')
            sys.exit(1)
       
        # get raster bands
        bands = ds.RasterCount
       
        # get georeference info
        transform = ds.GetGeoTransform()
        if batch == False:
            # line defining the profile
            line_file = ogr.Open(in_line)
            shape = line_file.GetLayer(0)
            #first feature of the shapefile
            line = shape.GetFeature(0)
            line_geom = line.geometry().ExportToWkt()
            shapely_line = LineString(wkt.loads(line_geom))
            # length in meters of profile line
            length_m = shapely_line.length
        else:
            line_geom = in_line.geometry().ExportToWkt()
            shapely_line = LineString(wkt.loads(line_geom))
            # length in meters of profile line
            length_m = shapely_line.length
        # lists of coords and elevations
        x = []
        y = []
        z = []
        # distance of the topographic profile
        distance = []
        for currentdistance in range(0, int(length_m), res):
            # creation of the point on the line
            point = shapely_line.interpolate(currentdistance)
            xp, yp = point.x, point.y
            x.append(xp)
            y.append(yp)
            # extraction of the elevation value from the MNT
            z.append(get_elevation(xp, yp, ds, bands, transform)[0])
            distance.append(currentdistance)  
       
        # combine distance and elevation vales as pairs
        profile_x_z = zip(distance,z)
       
        # output final csv data
        csv_file = os.path.join(save_folder, name+'.csv')
        write_to_csv(csv_file, profile_x_z)
    save_image = os.path.join(save_folder, 'profiles.png')
    make_profile_plot_mutliple(save_image, save_folder, NO_DATA)

def batch_main_raster(in_rasters, in_lines, save_folder, res, NO_DATA, batch=True):
    """
    Extracts elevation profiles given multiple input raster dems and an input shapefile containing mutliple lines
    inputs:
    in_raster_folder: list containing paths to raster dems
    in_line: path to shapefile containing profile lines
    save_folder: path to save results to (csvs, png figure)
    res: resolution to sample at in meters
    N0_DATA: raster no data value
    batch (optional): this should stay as False if just one profile is taken, use batch_main function for multiple profiles
    """
    line_file = ogr.Open(in_lines)
    layer = line_file.GetLayer(0)
    i=1
    for feature in layer:
        transect_folder = os.path.join(save_folder, 'transect'+str(i))
        os.mkdir(transect_folder)
        main_raster(in_rasters, feature, transect_folder, res, NO_DATA, batch=True)
        i=i+1



