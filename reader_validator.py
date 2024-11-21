from enums import DataTypes
from errors import NO_MATCHING_TYPE
from validators.tiff import TIFFValidator
from validators.vector import VectorValidator
import boto3

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
            self.data = VectorValidator(StringIO(self.download_s3_file(*self.parse_s3_path(filepath))))
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

    def parse_s3_path(self, s3_path):
        if not s3_path.startswith("s3://"):
            raise ValueError("Invalid S3 path format. Must start with 's3://'.")
        
        path = s3_path[5:]
        bucket, key = path.split("/", 1)
        return bucket, key

    def download_s3_file(self, bucket, key):
        """
        Download a file from S3 and return its content.
        Args:
            bucket (str): S3 bucket name.
            key (str): S3 object key.
        
        Returns:
            str: Content of the downloaded file.
        """
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
