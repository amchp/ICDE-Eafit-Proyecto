import os
import boto3
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

session = boto3.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    aws_session_token="",
    region_name="us-east-1"
)

class ReaderValidator:
    def __init__(self, data_type: DataTypes, s3_uri: str, temp_dir):
        self.type = data_type
        if not (data_type in VECTOR_TYPES or data_type in RASTER_TYPES):
            raise Exception(NO_MATCHING_TYPE)
        filepath = self.download_s3(s3_uri, temp_dir)
        if data_type in VECTOR_TYPES:
            self.data = VectorValidator(filepath)
            return
        if data_type in RASTER_TYPES:
            self.data = TIFFValidator(filepath)
            return

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

    def download_s3_folder(self, bucket, key, temp_dir):
        s3 = session.client("s3")
        response = s3.list_objects_v2(Bucket=bucket, Prefix=key)
        if 'Contents' not in response:
            raise FileNotFoundError(f"No files found in the specified folder: {key}")

        for obj in response['Contents']:
            file_key = obj['Key']
            relative_path = file_key[len(key):]  # Relative path within the folder
            local_file_path = os.path.join(temp_dir, relative_path)

            # Ensure directory structure is created
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download the file
            with open(local_file_path, 'wb') as f:
                s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=f)

        return temp_dir

    def download_s3_file(self, bucket, key, temp_dir):
        s3 = session.client("s3")
        file_name = os.path.basename(key)
        local_path = os.path.join(temp_dir, file_name)
        with open(local_path, 'wb') as f:
            s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=f)
        return local_path

    def download_s3(self, s3_uri, temp_dir):
        bucket, key = self.parse_s3_path(s3_uri)
        if key.endswith('/'):
            return self.download_s3_folder(bucket, key, temp_dir)
        else:
            return self.download_s3_file(bucket, key, temp_dir)
