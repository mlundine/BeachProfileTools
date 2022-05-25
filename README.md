# BeachProfileTools

Code to automate some useful beach analysis tasks.

# Anaconda Setup

First time, open Anaconda Prompt and run the following:

	conda env create --file BeachProfileTools.yml

All other times, activate this environment first:
	
	conda activate BeachProfileTools

Currently there are three modules that can be imported (import .... as ....).

# dem_to_shoreline

![shoreline](/images/shoreline.JPG)

	import dem_to_shoreline as dts

	dts.lidar_dem_to_shoreline(dem_path, 
				   contour_path, 
			           shoreline_path, 
				   no_data_value=-9999, 
				   filter_extra=False):
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

![transects](/images/transects.JPG)

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

# shoreline_timeseries

This module generates timeseries data and figures for shoreline change.

You need a shapefile with timestamped shorelines and a shapefile with one or multiple transects (for multiple, use the batch function).

The intersection points between each shoreline and the transect are computed. Then the cross-shore distance for each point is computed.

The earliest time shoreline intersection point is taken as the origin.

Outputs a figure of the timeseries and a csv with the data (time, eastings, northings, cross-shore distance).

Shown below is some fake data for Cape Henlopen:

![example_transects](/images/transects2.JPG)

![example_timeseries](/images/capehenlopen_2.png)

Batch function will output data and a figure for multiple transects.

![batch](/images/files.JPG)

	import shoreline_timeseries as sts

	sts.transect_timeseries(shoreline_shapefile,
                        transect_shapefile,
                        sitename,
                        transect_id,
                        output_folder,
                        switch_dir=False,
                        batch=False):
    	"""
    	Generates timeseries of shoreline cross-shore position
    	given a shapefile containing shorelines and a shapefile containing
    	a cross-shore transect. Computes interesection points between shorelines
    	and transect. Uses earliest shoreline intersection point as origin.
    
    	inputs:
    	shoreline_shapefile (str): path to shapefile containing shorelines
                               	   (needs a field 'datetime' YYYY-MM-DD-HH-MM)
    	transect_shapefile (str): path to shapefile containing cross-shore transect
    	sitename (str): name of site
    	transect_id (int): integer id for transect
    	output_folder (str): path to save csv and png figure to
    	switch_dir (optional): default is False, set to True if transects are in the opposite direction
    	batch (optional): default is False, this gets set to True when batch function is used
    	"""

	sts.batch_transect_timeseries(shorelines,
                              	  transects,
                              	  sitename,
                                  output_folder,
                                  switch_dir=False):
    	"""
    	Generates timeseries of shoreline cross-shore position
    	given a shapefile containing shorelines and a shapefile containing
    	cross-shore transects. Computes interesection points between shorelines
    	and transects. Uses earliest shoreline intersection point as origin.
    
    	inputs:
    	shoreline_shapefile (str): path to shapefile containing shorelines
                               	   (needs a field 'datetime' YYYY-MM-DD-HH-MM)
    	transect_shapefile (str): path to shapefile containing cross-shore transects
    	sitename (str): name of site
    	output_folder (str): path to save csvs and png figures to
    	switch_dir (optional): default is False, set to True if transects are in the opposite direction
    	"""
	