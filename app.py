import sqlite3
import pandas as pd
from django.contrib.auth.hashers import make_password

import os
from django import setup

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alemeno.settings')
setup()

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Read data from Excel file
excel_file = 'loan_data.xlsx'
df = pd.read_excel(excel_file)

# Iterate through the rows and insert into the SQLite database
for index, row in df.iterrows():
    loan_id = row['Loan ID']

    # Check if user with the given ID already exists
    cursor.execute("SELECT id FROM loan_loans WHERE id = ?", (loan_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"User with ID {loan_id} already exists. Skipping...")
        continue

    user_data = {
        'id': loan_id,  # You may need to adjust column names
        # 'email':
        'customer_id': row['Customer ID'],
        'loan_amount': row['Loan Amount'],
        'tenure': row['Tenure'],
        'interest_rate': row['Interest Rate'],
        'monthly_installment': row['Monthly payment'],
        'emis_paid_on_time': row['EMIs paid on Time'],
        'date_of_approval': row['Date of Approval'],
        'end_date': row['End Date'],
    }

    user_data['password'] = make_password('user_specific_password')

    # Convert Timestamp objects to strings
    # date_joined_str = user_data['date_joined'].strftime('%Y-%m-%d %H:%M:%S')
    # last_login_str = user_data['last_login'].strftime('%Y-%m-%d %H:%M:%S')

    # Insert data into the User table
   # Convert Timestamp objects to strings
    date_of_approval_str = str(user_data['date_of_approval'])
    end_date_str = str(user_data['end_date'])

    # Insert data into the User table
    cursor.execute("""
    INSERT INTO loan_loans (id, customer_id, loan_amount, tenure, interest_rate, monthly_installment, 
                            emis_paid_on_time, date_of_approval, end_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_data['id'],
        user_data['customer_id'],
        user_data['loan_amount'],
        user_data['tenure'],
        user_data['interest_rate'],
        user_data['monthly_installment'],
        user_data['emis_paid_on_time'],
        date_of_approval_str,  # Insert the string representation
        end_date_str,  # Insert the string representation
    ))

    # Commit the changes
    conn.commit()

# Close the connection
conn.close()
