from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigwv2,
    aws_dynamodb as ddb,
)

import aws_cdk as cdk

from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from constructs import Construct

class MovieDataApiStack(Stack):

    @property
    def handler(self):
        return self._handler

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = ddb.Table(self, 'MovieDataTable', removal_policy=cdk.RemovalPolicy.DESTROY, partition_key={'name': 'id', 'type': ddb.AttributeType.STRING} 
        )

        self._handler = _lambda.Function(
            self,
            "MovieDataFunction",
            runtime = _lambda.Runtime.PYTHON_3_8, 
            code = _lambda.Code.from_asset("lambda_handler"), 
            handler = "movie_data.handler", 
            environment={
                'tableName': table.table_name,
            }
        )

        
        movie_integration = HttpLambdaIntegration("MovieIntegration", self._handler)

        http_api = apigwv2.HttpApi(self, "HttpApi")

        http_api.add_routes(
            path="/movies",
            methods=[apigwv2.HttpMethod.GET],
            integration=movie_integration
        )
        
        http_api.add_routes(
            path="/movies/{releaseYear}",
            methods=[apigwv2.HttpMethod.GET],
            integration=movie_integration
        )


        table.grant_read_write_data(self._handler)


