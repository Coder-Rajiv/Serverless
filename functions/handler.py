import json
import logging
from .utils import BloggerFunctions

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def hello(event, context):
    try:
        logger.info(event)
        method = event["requestContext"]["http"]["method"]
        if event["body"]:
            body = json.loads(event["body"])
        else:
            body = event["pathParameters"]

        logger.info("Event payload read successfully")
        blog_object = BloggerFunctions()
        config_map = {
            "POST":blog_object.create_item,
            "PUT":blog_object.update_item,
            "DELETE":blog_object.delete_item,
            "GET":blog_object.read_item
        }
        
        response = config_map[method](email=body.get("email"),name=body.get("name"),blog=body.get("blog"))
        
        return response
    except Exception as err:
        logger.exception(str(err))
        return {
                "statusCode": 500, 
                "message":"Error", 
                "body": str(err)
            }
   