import os
import numpy as np
import earthpy.plot as ep
import rasterio as rio
from rasterio import Affine as A
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt

class FieldDetector:

    def __init__(self):
        pass

    ##################################################
    # Read 8-band Geotiff in UTM projection ##########

    def _read_geotiff(self):

        cwd = os.getcwd()
        tif_file = os.path.join(cwd, '20210827_162545_60_2262_3B_AnalyticMS_8b.tif') # Insert input file name here

        with rio.open(tif_file) as self.src:
            self.band_red = self.src.read(6) # Band 6: Red
            self.band_nir = self.src.read(8) # Band 8: Near Infrared (NIR)

            self.dst_crs = "EPSG:4326"
            print('Source raster CRS:', self.src.crs)
            print('Destination raster CRS:', self.dst_crs)

            self.transform, width, height = calculate_default_transform(
                self.src.crs, self.dst_crs, self.src.width, self.src.height, *self.src.bounds)

            # src_transform = src.transform
            # dst_transform = src_transform*A.translation(
            #     -src.width/2.0, -src.height/2.0)*A.scale(2.0)

            # Update spatial characteristics of the output object to be used later to reproject instead of mirroring input
            self.kwargs = self.src.meta.copy()
            self.kwargs.update({
                'dtype': rio.float32,
                'driver': 'GTiff',
                'transform': self.transform,
                'crs': self.dst_crs,
                'width': width*2.0,
                'height': height
            })

    ##################################################
    # Calculate NDVI #################################

    def _calculate_ndvi(self):

        np.seterr(divide='ignore', invalid='ignore') # Allow division by 0
        ndvi = (self.band_nir.astype(float) - self.band_red.astype(float)) / (self.band_nir + self.band_red) # NDVI calculation

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
        # Mean average NDVI: {mean_avg_nvdi}
        # Median average NDVI: {median_avg_nvdi}
        # Min NDVI: {min_nvdi}
        # Max NDVI: {max_nvdi}
        # NDVI histogram: {ndvi_histogram}
        """
        print(summary_stats)

        # Set threshold for normalize/rescaling NDVI values in array from [-1, 1] to either [0, 256]
        while True:
            try:        
                mid_threshold = float(input(f"Set a threshold between [{min_nvdi}, {max_nvdi}] to rescale NDVI values to [0, 255]: "))
                plt.close()
                default_upper_value = 255
                default_lower_value = 0
                ndvi[ndvi > mid_threshold] = default_upper_value
                ndvi[ndvi < mid_threshold] = default_lower_value
            except ValueError:
                print("Please enter a valid float")
                continue
            else:
                break

        return ndvi

    # ##################################################
    # # Output Geotiff file in EPSG 4326 projection ####

    def _output_geotiff(self):

        ndvi = self._calculate_ndvi()

        with rio.open('rescaled-ndvi.tif', 'w', **self.kwargs) as dst:
            # Assuming we can calculate NDVI first and pass it in when we reproject and write to a single band output
            # Otherwise, may need to reproject and output one new file, calculate NDVI, and output a second new file
            reproject(
                source=ndvi,
                destination=rio.band(dst, 1),
                src_transform=self.src.transform,
                src_crs=self.src.crs,
                dst_transform=self.transform,
                dst_crs=self.dst_crs,
                resampling=Resampling.nearest)

            print('Transform array of source raster: ', self.src.transform)
            print('Transform array of destination raster: ', self.transform)   
            print('Reprojected raster CRS:', dst.crs)

        ep.plot_bands(ndvi, cmap='RdYlGn', scale=False, title="Rescaled NDVI values to [0, 255]")
        plt.show()

        self.src.close()

    def run(self):
        self._read_geotiff()
        self._output_geotiff()
