aws lambda create-function \
  --function-name data-api \
  --package-type Image \
  --code ImageUri=884947855982.dkr.ecr.us-east-1.amazonaws.com/proyecto-maestria:latest \
  --role arn:aws:iam::884947855982:role/LabRole  \
  --architectures arm64
