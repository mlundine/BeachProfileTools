# BeachProfileTools

Code to automate some useful beach analysis tasks.

# Anaconda Setup

First time, open Anaconda Prompt and run the following:

	conda env create --file BeachProfileTools.yml

All other times, activate this environment first:
	
	conda activate BeachProfileTools

Currently there are three modules that can be imported (import .... as ....).

# dem_to_shoreline

![shoreline](/images/shoreline.jpg)

	import dem_to_shoreline as dts

	dts.lidar_dem_to_shoreline(dem_path, contour_path, shoreline_path, no_data_value=-9999, filter_extra=False)
	"""
	Uses gdal to take a raster DEM (.tif, .img, Esri grids, etc.)
    	and generate contours. Then extracts the 0 contour as the shoreline.
    	If data includes areas that have low spots other than the shore
    	(ex: ponds inland from dune), then can filter out the longest 0 contour as shoreline.
    	inputs:
    	dem_path: path to the dem (str)
    	contour_path: path to save all of the contours to, end this with .shp (str)
    	shoreline_path: path to save the 0 contour to, end with .shp (str)
    	no_data_value (optional, default=-9999): the no data value for the raster 
    	filter_extra (optional, default=False): If set to True, will only save the longest 0 contour to the shoreline file
	"""

# generating_transects

![shoreline](/images/transects.jpg)

	import generating_transects as gen_tr
	
	gen_tr.make_transects(input_path,
                   transect_spacing,
                   transect_length):
    	"""
    	Generates normal transects to an input line shapefile
    	inputs:
    	input_path: path to shapefile containing the input line
    	transect_spacing: distance between each transect in meters
    	transect_length: length of each transect in meters
    	outputs:
    	output_path: path to output shapefile containing transects

# profile_raster

![profile](/images/profiles.png)

	import profile_raster

	profile_raster.main(in_raster, in_line, csv_file, res, NO_DATA, batch=False):
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
	
	profile_raster.batch_main(in_raster, in_lines, out_folder, res, NO_DATA):
    	"""
    	Repeatedly take elevation profiles from a raster dem with an input shapefile containing all of the lines
    	inputs:
    	in_raster: path to raster dem
    	in_lines: path to shapefile containing profile lines
    	out_folder: path to folder to save csvs and png figures to
    	res: resolution to sample at in meters
    	NO_DATA: no data value for raster
    	"""

	profile_raster.main_raster(in_rasters, in_line, save_folder, res, NO_DATA, batch=False):
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

	profile_raster.batch_main_raster(in_rasters, in_lines, save_folder, res, NO_DATA, batch=True):
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