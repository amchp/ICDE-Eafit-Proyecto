# main.py
from osgeo import ogr
import os

ogr.UseExceptions()

# Path to the File Geodatabase (.gdb file)
for filename in os.listdir('/app'):
    print(filename)

gdb_path = "/app/files/Productos_Vigentes.gdb"


# Open the File Geodatabase
driver = ogr.GetDriverByName("OpenFileGDB")
data_source = driver.Open(gdb_path, 0)  # 0 means read-only mode

if data_source is None:
    print("Could not open the .gdb file.")
else:
    # Print the layer names in the GDB file
    print("Layers in the File Geodatabase:")
    for layer_index in range(data_source.GetLayerCount()):
        layer = data_source.GetLayerByIndex(layer_index)
        layer_name = layer.GetName()
        print(f"Layer {layer_index + 1}: {layer_name}")

        # Read features in the layer
        for feature in layer:
            print("Feature:", feature.GetFID())
            for i in range(feature.GetFieldCount()):
                field_name = feature.GetFieldDefnRef(i).GetName()
                field_value = feature.GetField(i)
                print(f"  {field_name}: {field_value}")

