import requests_mock
import unittest2
from mock import patch, call, Mock, MagicMock

from terminate_wait import handler

LIFECYCLE_HOOK_NAME = 'AStroubleshoot'
LIFECYCLE_TRANSACTION_TERMINATING = 'autoscaling:EC2_INSTANCE_TERMINATING'


class CreateTests(unittest2.TestCase):

    @patch('boto3.client')
    @requests_mock.Mocker()
    def test_create_terminate_wait(self, boto_client_mock, request_mock):
        client_mock = Mock()
        boto_client_mock.return_value = client_mock

        create_mock = client_mock.put_lifecycle_hook = MagicMock()
        iam_mock = client_mock.get_user = MagicMock()
        iam_mock.return_value = {'User': {'Arn':
                                          "arn:aws:iam::123456:role/abc"}}
        create_event = {
            'RequestId': 'anyId',
            'StackId': 'StackID',
            'LogicalResourceId': 'logicID',
            "ResourceProperties": {
                "AutoScalingGroupName": 'ASGName'
            },
            "RequestType": "Create",
            "ResponseURL": "https://response_url"
        }

        context_mock = Mock()
        request_mock.put('https://response_url', status_code=200, text='ok')

        handler(create_event, context_mock)

        create_mock.assert_called_with(
          LifecycleHookName=LIFECYCLE_HOOK_NAME,
          AutoScalingGroupName='ASGName',
          LifecycleTransition=LIFECYCLE_TRANSACTION_TERMINATING,
          RoleARN="arn:aws:iam::123456:role/ASTroubleshootRole",
          NotificationTargetARN=(
            "arn:aws:sns:eu-west-1:123456:ASTroubleshootTopic"),
          NotificationMetadata='setting ec2 in wait state',
          HeartbeatTimeout=3600
        )
        iam_mock.assert_has_calls([
            call(),
            call()
        ])

    @patch('boto3.client')
    @requests_mock.Mocker()
    def test_delete_terminate_wait(self, boto_client_mock, request_mock):
        client_mock = Mock()
        boto_client_mock.return_value = client_mock

        delete_mock = client_mock.complete_lifecycle_action = MagicMock()
        delete_event = {
            'RequestId': 'anyId',
            'StackId': 'StackID',
            'LogicalResourceId': 'logicID',
            "ResourceProperties": {
                "AutoScalingGroupName": 'ASGName'
            },
            "RequestType": "Delete",
            "ResponseURL": "https://response_url"
        }

        context_mock = Mock()
        request_mock.put('https://response_url', status_code=200, text='ok')

        handler(delete_event, context_mock)

        delete_mock.assert_called_with(
          LifecycleHookName=LIFECYCLE_HOOK_NAME,
          AutoScalingGroupName='ASGName',
          LifecycleActionResult='CONTINUE'
        )
