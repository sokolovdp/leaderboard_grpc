protoc --proto_path=proto --python_out=proto proto/*.proto
python -m grpc_tools.protoc --proto_path=proto --python_out=proto --grpc_python_out=proto proto/*.proto