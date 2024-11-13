from readers.vector import VectorValidator
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

filepaths = [
    "/app/files/Productos_Vigentes.gdb",
    "/app/files/Carto1000_15001000_RS_20220119.gpkg",
    "/app/files/Carto1000_15001000_RS_20220119_shp",
    "/app/files/KML_Samples.kml",
]

for filepath in filepaths:
    print(f"Processing file: {filepath}", flush=True)
    vector_validator = VectorValidator(filepath)
    print(vector_validator.check_spatial_reference_consistency())
