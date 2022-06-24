from dataclasses import dataclass, field
import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="Hello-App")
app = APIGatewayRestResolver()

# import requests


def hello_name(event, **kwargs):
    username = event["pathParameters"]["name"]
    return {"statusCode": 200, "body": json.dumps({"message": f"Welcome {username}"})}


def hello(**kwargs):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": f"hello Unknown",
            }
        ),
    }


@dataclass
class Router:
    routes: dict = field(default_factory=dict)

    def set(self, path, method, handler):
        self.routes[f"{path}-{method}"] = handler

    def get(self, path, method):
        try:
            route = self.routes[f"{path}-{method}"]
        except KeyError:
            raise RuntimeError("method or path not found")
        return route


router = Router()
router.set(path="/hello", method="GET", handler=hello)
router.set(path="/hello/{name}", method="GET", handler=hello_name)


def lambda_handler(event, context):
    """Sample pure Lambda function"""
    path = event["resource"]
    http_method = event["httpMethod"]

    handler = router.get(path, http_method)

    print(handler)
    return handler(event=event)
