from enums import DataTypes
from errors import NO_MATCHING_TYPE
from validators.tiff import TIFFValidator
from validators.vector import VectorValidator

VALIDATION_MATRIX = {
    DataTypes.GDB: [
        ("consistencia_de_origen", VectorValidator.check_spatial_reference_consistency),
    ],
    DataTypes.Poligon: [
        ("valores_nulos", VectorValidator.check_null_fields),
        ("dentro_de_origen", VectorValidator.check_inside_colombia),
        ("consistencia_de_origen", VectorValidator.check_spatial_reference_consistency),
        ("hueco_en_capa", VectorValidator.check_gaps),
        ("superposicion", VectorValidator.check_overlap),
    ],
    DataTypes.Line: [
        ("valores_nulos", VectorValidator.check_null_fields),
        ("dentro_de_provedor", VectorValidator.check_inside_colombia),
        ("consistencia_de_origen", VectorValidator.check_spatial_reference_consistency),
        ("superposicion", VectorValidator.check_overlap),
    ],
    DataTypes.Point: [
        ("valores_nulos", VectorValidator.check_null_fields),
        ("dentro_de_origen", VectorValidator.check_inside_colombia),
        ("consistencia_de_origen", VectorValidator.check_spatial_reference_consistency),
        ("superposicion", VectorValidator.check_overlap),
    ],
    DataTypes.DigitalTerainModel: [
        ("dentro_de_provedor", TIFFValidator.check_if_inside_colombia),
        ("consistencia_de_origen", TIFFValidator.check_spatial_reference_consistency),
    ],
    DataTypes.Ortoimages: [
        ("dentro_de_provedor", TIFFValidator.check_if_inside_colombia),
        ("consistencia_de_origen", TIFFValidator.check_spatial_reference_consistency),
        ("bandas", TIFFValidator.check_bands),
        ("radiometria", TIFFValidator.check_radiometric_resolution),
    ]
}

VECTOR_TYPES = [DataTypes.GDB, DataTypes.Poligon, DataTypes.Line, DataTypes.Point]
RASTER_TYPES = [DataTypes.DigitalTerainModel, DataTypes.Ortoimages]

class ReaderValidator:
    def __init__(self, data_type: DataTypes, filepath: str):
        self.type = data_type
        if data_type in VECTOR_TYPES:
            self.data = VectorValidator(filepath)
            return
        if data_type in RASTER_TYPES:
            self.data = TIFFValidator(filepath)
            return
        raise Exception(NO_MATCHING_TYPE)

    def validate(self):
        errors = {}
        for error, method in VALIDATION_MATRIX[self.type]:
            try:
                errors[error] = method(self.data)
            except Exception as err:
                errors["error_de_sistema"] = err
        return errors
