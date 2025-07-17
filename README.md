# Data Ingestion from API

## How to Run the Script
1. Create virtual environment

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a new `.env` file with the same keys as `sample.env`, and replace the values with your own credentials

4. Run main.py script
    ```bash
    python main.py
    ```
    output:
    ```
    Data directory is not exists
    Initailizing data directory...
    ===================================
    Attempting to call Ekraf API...
    API call successful!
    Raw data saved in local path: data/raw_data_2025_07_17.json
    ===================================
    Transforming data...
    Data transform successful!
    Transformed data saved in local path: data/transformed_data_2025_07_17.json
    ===================================
    Attempting to create a connection to SFTP Server...
    Connection created successfully!
    Data loaded from local path: data/transformed_data_2025_07_17.json to remote path: /uploads/transformed_data_2025_07_17.csv
    ```