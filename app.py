from enums import DataTypes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from reader_validator import ReaderValidator

app = FastAPI()

class InputModel(BaseModel):
    data_type: int = Field(..., description="An integer representing the data type")
    s3_bucket_uri: str = Field(..., description="The URI of the S3 bucket")

@app.post("/process-data/")
async def process_data(input_data: InputModel):
    if not input_data.s3_bucket_uri.startswith("s3://"):
        raise HTTPException(status_code=400, detail="Invalid S3 bucket URI")
    try:
        rv = ReaderValidator(
            DataTypes(input_data.data_type),
            input_data.s3_bucket_uri
        )
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

    result = rv.validate()

    return result
