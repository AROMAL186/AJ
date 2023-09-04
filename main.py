from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

app = Flask(__name__)

# Define the scope and the path to your JSON key file (credentials)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('AJ.json', scope)

# Authenticate with Google Sheets
gc = gspread.authorize(credentials)

# Open the Google Sheets spreadsheet by title
spreadsheet = gc.open('AJ')

# Select a worksheet by title or index (e.g., the first worksheet)
worksheet = spreadsheet.get_worksheet(0)

# Load existing data from JSON if available
try:
    with open('registration_data.json', 'r') as json_file:
        registration_data = json.load(json_file)
except FileNotFoundError:
    registration_data = []

@app.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']

        # Data to write to Google Sheets
        data = [first_name, last_name, email]

        # Append the data to the worksheet
        worksheet.append_row(data)

        # Store the data in a JSON file
        registration_data.append({'First Name': first_name, 'Last Name': last_name, 'Email': email})
        with open('registration_data.json', 'w') as json_file:
            json.dump(registration_data, json_file, indent=4)

        return render_template('registration_success.html')

    return render_template('registration_form.html')

if __name__ == '__main__':
    app.run(debug=True)
