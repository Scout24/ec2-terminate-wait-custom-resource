import livecycle_hook


def handler(event, context):
    request_type = event['RequestType']
    properties = event['ResourceProperties']
    asg_name = properties['AutoScalingGroupName']

    if request_type == 'Create':
        livecycle_hook.activate_terminate_wait_hook(asg_name)
    elif request_type == 'Delete':
        livecycle_hook.deactivate_terminate_wait_hook(asg_name)
