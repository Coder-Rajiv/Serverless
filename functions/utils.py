import json
import boto3

class BloggerFunctions:
    def  __init__(self):
        self.table_name = "blog_data_table"
        self.dynamodb = boto3.client(
                            "dynamodb", 
                            region_name='localhost', 
                            endpoint_url= 'http://localhost:8000',
                            aws_access_key_id='DEFAULT_ACCESS_KEY',
                            aws_secret_access_key= 'DEFAULT_SECRET'
                            )

    def create_item(self,**kwargs):
        self.dynamodb.put_item(
                    TableName=self.table_name,
                    Item={
                            'Email': {'S': kwargs["email"]},
                            'Name' : {'S':kwargs["name"]},
                            'Description':{'S':kwargs["blog"]}
                    })

        return {"statusCode": 200, "body": "Data added in dynaomdb Successfully"}

    def read_item(self,**kwargs):
        response = self.dynamodb.get_item(
                                            TableName=self.table_name,
                                            Key={
                                                'Email': {'S': kwargs["email"]}
                                            }
                                                
                                    )
        if response.get("Item"):
            status_code = 200
            msg = f"Authored: {response['Item']['Name']['S']}\n\nBlog:\n\n\t{response['Item']['Description']['S']}"
        else:
            status_code = 404
            msg = f'No data found for Email: {kwargs["email"]}'

        return {"statusCode": status_code, "message":"Read Successfully", "body": msg}

    def update_item(self,**kwargs):
        response  = self.read_item(email=kwargs["email"])
        if response["statusCode"]==200:
            response =    self.dynamodb.update_item(
                                                TableName=self.table_name,
                                                Key={'Email': {'S': kwargs["email"]}},
                                                UpdateExpression="SET Description = :Description",
                                                ExpressionAttributeValues={':Description': {'S':kwargs["blog"]}},
                                                ReturnValues="UPDATED_NEW"
                                            )
        
            return {
                "statusCode": 200, 
                "message":"Updated Successfully", 
                "body": json.dumps(response)
            }
        else:
            return response

    def delete_item(self,**kwargs):
        response  = self.read_item(email=kwargs["email"])
        if response["statusCode"]==200:
            response = self.dynamodb.delete_item(
                                        TableName=self.table_name,
                                        Key={'Email': {'S': kwargs["email"]}},
                                        ReturnValues="ALL_OLD"
                                    )
            return {
                "statusCode": 200,
                "message":"Deleted Successfully",
                "body": json.dumps(response)
                }
        else:
            return response