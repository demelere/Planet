### To replicate:
1. Start virtual environment
2. From project root directory run `pip install -r /path/to/requirements.txt`
3. Copy and paste input .tif file into project root directory
4. Call FieldDetector code from a separate script (ex: `separate_script.py`) by:
    - importing the class from the module `from field_detector import FieldDetector`
    - instantiating the class instance to a variable `field_detector = FieldDetector()`
    - calling the run method `field_detector.run()` 
5. From project root directory run `python3 separate_script.py`

### Notes:
I built a rudimentary agricultural field detector that takes 8-band geotiff images in UTM projection, calculates NDVI values, and outputs a geotiff in lat/long (EPSG 4326) projection. 
* NDVI values will be high where there are plants and lower where they are absent.
* Pixels in the output images have a value of 255 where fields are located and 0 elsewhere.
* Includes client input to specify the threshold for determining which NDVI values should be considered as part of a field.

### References:
https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
* NDVI = (NIR - R) / (NIR + R)
* NIR = Near Infrared
* R = Red
* Band order in given image
    * Band 1: Coastal Blue
    * Band 2: Blue
    * Band 3: Green I
    * Band 4: Green
    * Band 5: Yellow
    * Band 6: Red
    * Band 7: Red Edge
    * Band 8: Near Infrared (NIR)
