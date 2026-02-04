import boto3

def list_my_buckets():
    # Initialize the S3 client
    # It automatically looks for credentials in your ~/.aws/credentials file
    s3 = boto3.client('s3')

    try:
        # Call AWS to get the list of buckets
        response = s3.list_buckets()

        print("--- Your S3 Buckets ---")
        
        # The response is a dictionary; the 'Buckets' key contains the list
        for bucket in response['Buckets']:
            print(f"Bucket Name: {bucket['Name']}")
            
    except Exception as e:
        print(f"Error connecting to AWS: {e}")

if __name__ == "__main__":
    list_my_buckets()