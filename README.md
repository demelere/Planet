### To replicate:
1. Start virtual environment
2. From project root directory run `pip install -r /path/to/requirements.txt`
3. Copy and paste input .tif file into project root directory
4. Call FieldDetector code from a separate script (ex: `separate_script.py`) by:
    - importing the class from the module `from field_detector import FieldDetector`
    - instantiating the class instance to a variable `field_detector = FieldDetector()`
    - calling the run method `field_detector.run()` 
5. From project root directory run `python3 separate_script.py`