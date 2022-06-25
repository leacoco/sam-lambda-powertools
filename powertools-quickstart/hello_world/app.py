from dataclasses import dataclass, field
import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="Hello-App")
app = APIGatewayRestResolver()

# import requests


@app.get("/hello/<name>")
def hello_name(name):
    logger.info(f"Request for {name} received")
    return {"message": f"Welcome {name}"}


@app.get("/hello")
def hello():
    logger.info("Request from unknown")
    return {"message": "Hello unknown"}


# @dataclass
# class Router:
#     routes: dict = field(default_factory=dict)

#     def set(self, path, method, handler):
#         self.routes[f"{path}-{method}"] = handler

#     def get(self, path, method):
#         try:
#             route = self.routes[f"{path}-{method}"]
#         except KeyError:
#             raise RuntimeError("method or path not found")
#         return route


# router = Router()
# router.set(path="/hello", method="GET", handler=hello)
# router.set(path="/hello/{name}", method="GET", handler=hello_name)


@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
def lambda_handler(event, context):
    """Sample pure Lambda function"""
    return app.resolve(event, context)
