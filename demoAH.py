import boto3

# Khởi tạo client DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id="aws_access_key_id",
    aws_secret_access_key="aws_secret_access_key",
    region_name="us-west-2"
)

# Tạo bảng DynamoDB
def create_table():
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'UserId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'UserName',
                'KeyType': 'RANGE'  # Sort key (nếu có)
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'UserName',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Chờ bảng được tạo xong
    table.meta.client.get_waiter('table_exists').wait(TableName='Users')
    print(f"Bảng {table.table_name} đã được tạo thành công!")

def add_user(user_id, user_name):
    table = dynamodb.Table('Users')
    table.put_item(
        Item={
            'UserId': user_id,
            'UserName': user_name,
            'Age': 30,
            'City': 'New York'
        }
    )
    print(f"Thêm người dùng {user_name} thành công!")


def get_user(user_id, user_name):
    table = dynamodb.Table('Users')
    response = table.get_item(
        Key={
            'UserId': user_id,
            'UserName': user_name
        }
    )

    item = response.get('Item')
    if item:
        print(f"Thông tin người dùng: {item}")
    else:
        print(f"Không tìm thấy người dùng với ID: {user_id}")

def update_user(user_id, user_name, new_city):
    table = dynamodb.Table('Users')
    table.update_item(
        Key={
            'UserId': user_id,
            'UserName': user_name
        },
        UpdateExpression='SET City = :val1',
        ExpressionAttributeValues={
            ':val1': new_city
        }
    )
    print(f"Đã cập nhật thành phố cho người dùng {user_name} thành {new_city}")

def delete_user(user_id, user_name):
    table = dynamodb.Table('Users')
    table.delete_item(
        Key={
            'UserId': user_id,
            'UserName': user_name
        }
    )
    print(f"Đã xóa người dùng {user_name}")





create_table()
add_user('002', 'Nghia Nguyen')
get_user('001', 'John Doe')
update_user('001', 'John Doe', 'Los Angeles')
delete_user('001', 'John Doe')



