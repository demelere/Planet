Coding Task for Geospatial Software Engineer

Your task is to write a rudimentary agricultural field detector. Do this by calculating NDVI for a given 8-band image. NDVI values will be high where there are plants and lower where they are absent.

Given an 8-band geotiff in UTM projection, calculate NDVI and output a geotiff one in Lat/Long (EPSG 4326) projection.
Pixels in output images should have a value of 255 where fields are located and 0 elsewhere.
Code must be importable/callable from a separate script.
Code must allow client code to specify the threshold for determining which NDVI values should be considered as part of a field.

The code does not need to find the fields perfectly. There will likely be some false positives and false negatives.

Helpful Info:
https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index

NDVI = (NIR - R) / (NIR + R)
NIR = Near Infrared
R = Red

Band order in given image
Band 1: Coastal Blue
Band 2: Blue
Band 3: Green I
Band 4: Green
Band 5: Yellow
Band 6: Red
Band 7: Red Edge
Band 8: Near Infrared (NIR)
