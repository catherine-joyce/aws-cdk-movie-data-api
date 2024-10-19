import aws_cdk as core
import aws_cdk.assertions as assertions

from movie_data_api.movie_data_api_stack import MovieDataApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in movie_data_api/movie_data_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MovieDataApiStack(app, "movie-data-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
