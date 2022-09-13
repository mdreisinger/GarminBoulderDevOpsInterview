"""
Send an email using boto3.
"""
import boto3
from botocore.exceptions import ClientError

# This address must be verified with Amazon SES.
SENDER = "Test McTester <testymctester653@gmail.com>"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"

# The character encoding for the email.
CHARSET = "UTF-8"

def email_service(recipient, subject, body_text):
    """
    @param recipient If your account is still in the sandbox, this address must be verified.
    @param subject The subject line for the email.
    @param body_text The email body for recipients with non-HTML email clients.
    """
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as error:
        print(error.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])
