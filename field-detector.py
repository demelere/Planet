import os
import numpy as np
import earthpy.plot as ep
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt

# class FieldDetector():
#     def __init__(self):
#         self.dst_crs = "EPSG:4326"

#     def read_geotiff():

##################################################
# Read 8-band Geotiff in UTM projection ##########
cwd = os.getcwd()
tif_file = os.path.join(cwd, '20210827_162545_60_2262_3B_AnalyticMS_8b.tif')

# src = rio.open(tif_file)
# band_red = src.read(6) # Band 6: Red
# band_nir = src.read(8) # Band 8: Near Infrared (NIR)

with rio.open(tif_file) as src:
    band_red = src.read(6) # Band 6: Red
    band_nir = src.read(8) # Band 8: Near Infrared (NIR)

    dst_crs = "EPSG:4326"
    print('source raster crs:', src.crs)
    print('destination raster crs:', dst_crs)

    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)

    # Update spatial characteristics of the output object to reproject instead of mirroring input
    kwargs = src.meta.copy()
    kwargs.update({
        'dtype': rio.float32, # You should either initialize your raster as dtype=rasterio.float32 , or multiply your values by 1000 in your code, ans store as int16.
        # 'count': 1, # do i need to change this one?
        'driver': 'GTiff',
        'transform': transform,
        'crs': dst_crs,
    })
    # 'width': width,
    # 'height': height

##################################################
# Calculate NDVI #################################

np.seterr(divide='ignore', invalid='ignore') # Allow division by 0
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red) # NDVI calculation

# Show histogram and summary statistics before requesting threshold user input
ep.hist(ndvi, colors='lightblue' ,figsize=(12, 6),
        title=["Distribution of unscaled NDVI values from [-1, 1]"])
plt.suptitle('Set a threshold in the terminal to rescale to [0, 255]', y=0.85)
plt.show(block=False)

ndvi_summary_stats = ndvi[~np.isnan(ndvi)]
mean_avg_nvdi = round(np.mean(ndvi_summary_stats),2)
median_avg_nvdi = round(np.median(ndvi_summary_stats), 2)
min_nvdi = round(np.min(ndvi_summary_stats), 2)
max_nvdi = round(np.max(ndvi_summary_stats), 2)
ndvi_histogram = np.histogram(ndvi_summary_stats)

summary_stats = f"""
# NDVI summary statistics
# mean average ndvi: {mean_avg_nvdi}
# median average ndvi: {median_avg_nvdi}
# mean average ndvi: {min_nvdi}
# mean average ndvi: {max_nvdi}
# ndvi histogram: {ndvi_histogram}
"""
print(summary_stats)

# Set threshold for normalize/rescaling NDVI values in array from [-1, 1] to either [0, 256]
mid_threshold = float(input(f"Set a threshold between [{min_nvdi}, {max_nvdi}] to rescale NDVI values to [0, 255]: "))
plt.close()
default_upper_value = 255
default_lower_value = 0
ndvi[ndvi > mid_threshold] = default_upper_value
ndvi[ndvi < mid_threshold] = default_lower_value

# ##################################################
# # Output Geotiff file in EPSG 4326 projection ####

with rio.open('rescaled-ndvi.tif', 'w', **kwargs) as dst:
    # Assumes reprojection doesn't need to be handled first
    # 
    # + ndvi as just a single band
    # instead of write_band

    # we should handle reprojection first
    # then calculate ndvi 
    # then write ndvi to single band output

    

    reproject(
        source=ndvi,
        destination=rio.band(dst, 1),
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest)
 
    print('transform array of source raster: ', src.transform)
    print('transform array of destination raster: ', transform)   
    print('reprojected raster crs:', dst.crs)

ep.plot_bands(ndvi, cmap='RdYlGn', scale=False, title="Rescaled NDVI values to [0, 255]")
plt.show()

src.close()