from flask import Flask, render_template, request
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

csv_file_path = os.getenv('FILE_LOCATION')
mapbox_token = os.getenv('MAPBOX_TOKEN')


app = Flask(__name__)

@app.route('/')
def show_map_from_ssid():
    ssid = request.args.get('ssid', '').strip()
    limit = request.args.get('limit', type=int, default=100)

    # Load the CSV data
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()

    # Filter the dataframe for the given SSID
    filtered_df = df[
        (df['SSID'].notna()) &
        (df['SSID'].str.strip().str.upper().str.contains(ssid.upper())) &
        (df['Type'].str.strip().str.upper() == 'WIFI')
    ]

    # Select relevant columns
    df_filtered = filtered_df[['SSID', 'CurrentLatitude', 'CurrentLongitude', 'Type', 'MAC']].dropna()

    # Remove duplicate MAC addresses
    df_filtered = df_filtered.drop_duplicates(subset='MAC')

    # Limit the result
    df_filtered = df_filtered.head(limit)

    networks = df_filtered.to_dict(orient='records')

    return render_template('index.html', networks=networks, ssid=ssid, limit=limit, mapbox_token=mapbox_token)

if __name__ == '__main__':
    app.run(debug=True)
