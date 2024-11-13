from osgeo import gdal

class TIFFValidator:
    def __init__(self, filepath):
        self.dataset = gdal.Open(filepath, gdal.GA_ReadOnly)
    
        if not self.dataset:
            raise FileNotFoundError(f"Could not open file: {filepath}")

    def reader(self):
        # Get layer count and display
        width = self.dataset.RasterXSize
        height = self.dataset.RasterYSize
        band_count = self.dataset.RasterCount
        projection = self.dataset.GetProjection()
        geotransform = self.dataset.GetGeoTransform()
        
        print(f"Width: {width}")
        print(f"Height: {height}")
        print(f"Number of bands: {band_count}")
        print(f"Projection: {projection}")
        print(f"GeoTransform: {geotransform}")
        if geotransform:
            origin_x = geotransform[0]
            origin_y = geotransform[3]
            pixel_width = geotransform[1]
            pixel_height = geotransform[5]
            print("\nGeoTransform Interpretation:")
            print(f"  Origin (Top-Left Corner): ({origin_x}, {origin_y})")
            print(f"  Pixel Size: ({pixel_width}, {pixel_height})")
        
        # Read each band and print statistics
        for i in range(1, band_count + 1):
            band = self.dataset.GetRasterBand(i)
            min_val, max_val, mean_val, stddev_val = band.GetStatistics(True, True)
            print(f"\nBand {i} Statistics:")
            print(f"  Min: {min_val}")
            print(f"  Max: {max_val}")
            print(f"  Mean: {mean_val}")
            print(f"  StdDev: {stddev_val}")
            
            # Optionally, read the pixel data (example: read the first row)
            first_row = band.ReadAsArray(0, 0, width, 1)
            print(f"  First row of pixel values: {first_row[0]}")  # Display first row of pixels
