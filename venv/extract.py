from faker import Faker
import random
import string
import csv
from google.cloud import storage

# Specify number of employees to generate
num_employees = 100

# Create a Faker instance
fake = Faker()

# Define the character set for the password
password_characters = string.ascii_letters + string.digits + 'm'

# Predefined list of departments to avoid commas
departments = [
    "HR",
    "Engineering",
    "Sales",
    "Marketing",
    "Finance",
    "Support",
    "IT",
    "Legal",
    "Operations",
    "Management"
]

# Generate employee data and save it to CSV file
with open('employee_data.csv', mode='w', newline='') as file:
    fieldnames = ['first_name', 'last_name', 'job_title', 'department', 'email', 'address', 'phone_number', 'salary', 'password']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for _ in range(num_employees):
		# Remove commas from job titles
        job_title = fake.job().replace(',', '')
        department = random.choice(departments)
        writer.writerow({
            "first_name": fake.first_name().replace(',', ''),
            "last_name": fake.last_name().replace(',', ''),
            "job_title": job_title,
            "department": department,
            "email": fake.email().replace(',', ''),
            "address": fake.city().replace(',', ''),
            "phone_number": fake.phone_number().replace(',', ''),
            "salary": fake.random_number(digits=5),
            "password": ''.join(random.choice(password_characters) for _ in range(8))
        })

print(f"Data saved to employee_data.csv")

# Upload CSV file to a GCS bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')

# Set GCS bucket name and destination file name
bucket_name = 'buket-employee-data'
source_file_name = 'employee_data.csv'
destination_blob_name = 'employee_data.csv'

# Upload CSV file to GCS
upload_to_gcs(bucket_name, source_file_name, destination_blob_name)