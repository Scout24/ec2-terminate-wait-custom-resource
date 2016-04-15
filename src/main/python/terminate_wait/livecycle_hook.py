import boto3

LIFECYCLE_HOOK_NAME = 'AStroubleshoot'
LIFECYCLE_TRANSACTION_TERMINATING = 'autoscaling:EC2_INSTANCE_TERMINATING'


def activate_terminate_wait_hook(autoscaling_group_name,
                                 region='eu-west-1',
                                 role_name='ASTroubleshootRole',
                                 notification_topic_name='ASTroubleshootTopic',
                                 transaction=LIFECYCLE_TRANSACTION_TERMINATING,
                                 heartbeat_timeout=3600):
    client = boto3.client('autoscaling')
    response = client.put_lifecycle_hook(
          LifecycleHookName=LIFECYCLE_HOOK_NAME,
          AutoScalingGroupName=autoscaling_group_name,
          LifecycleTransition=transaction,
          RoleARN=_role_arn(role_name),
          NotificationTargetARN=_notification_target_arn(
              notification_topic_name,
              region),
          NotificationMetadata='setting ec2 in wait state',
          HeartbeatTimeout=heartbeat_timeout)

    return response


def deactivate_terminate_wait_hook(autoscaling_group_name,
                                   action_result='CONTINUE'):
    client = boto3.client('autoscaling')
    response = client.complete_lifecycle_action(
        LifecycleHookName=LIFECYCLE_HOOK_NAME,
        AutoScalingGroupName=autoscaling_group_name,
        LifecycleActionResult=action_result)

    return response


def _account_id():
    return boto3.client('iam').get_user()['User']['Arn'].split(':')[4]


def _role_arn(role_name):
    return "arn:aws:iam::{0}:role/{1}".format(_account_id(), role_name)


def _notification_target_arn(notification_target_name, region):
    return "arn:aws:sns:{0}:{1}:{2}".format(region,
                                            _account_id(),
                                            notification_target_name)
