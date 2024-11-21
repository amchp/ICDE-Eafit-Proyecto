SUFFIX_ERROR = (
    "El archivo no se pudo leer porque no es de los tipos acceptados para vector." \
    "Los tipos aceptados para vector son shp, gdb, gpkg, kml, y dxf."
)
COULD_NOT_READ_FILE_ERROR = "No se pudo leer el archivo"
NO_MATCHING_TYPE = "El tipo de archivo no coincide con los especificados"
NULL_FIELD_ERROR = "La capa {layer_name} en la columna {column_name} tiene un valor nulo"
SPATIAL_REFERENCE_INCONSISTENCY = (
    "Existe una incosistencia entre el punto de origen de de la capa {first_layer_name} y {layer_name}"
)
OUTSIDE_COLOMBIA = "La capa '{layer_name}' tiene geometrías fuera de Colombia."
INVALID_SPATIAL_REFERENCE = (
    "El punto de origen del archivo no se es validos." \
    "Los puntos de origen validos son EPSG:9377, EPSG:4686, EPSG:3118, EPSG:3117, EPSG:3115, EPSG:3114."
)
OVERLAP_ERROR = "Superposition en el archivo"
GAP_ERROR = "Hueco en la capa {layer_name}"
OUTSIDE_COLOMBIA_TIFF = "El raster esta fuera de Colombia"
BANDS_ERROR = "La Ortoimagen no tiene las tres minimas bandas rojo, azul y verde"
RADIOMETRIC_ERROR = "La Ortoimagen no tiene la minima resolución de radiometria"
