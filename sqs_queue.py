import logging
import boto3
from botocore.exceptions import ClientError


def send_sqs_message(sqs_queue_url, msg_body):
    """
    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """
    sqs_client = boto3.client('sqs', region_name='us-east-1')
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body)
    except ClientError as e:
        logging.error(e)
        return None

    return msg
