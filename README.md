# Socialite
### By Suyogya Poudel
A X (formerly twitter) inpsired social media application
---
Requirements
  ```
  Python: >= v3.9.5
  Node: >= v14.6.1
  PostgreSQL: v14.15
  ```
Other Requirements
- Supabase: https://supabase.com/dashboard/sign-in?returnTo=%2Fprojects
  - Database
  - Detailed instruction in `docs/supabase/` directory

- GeoIP: https://www.maxmind.com/en/account/sign-in
  - Used to determine where user logged in from for all their sessions
    - Device
    - City
    - State
  - Download Database from MaxMind after logging in
    - GeoLite2 City - file name: GeoLite2-City.mmdb
    - GeoLite2 Country - file name: GeoLite2-Country.mmdb

- AWS Account:
  - Instruction to create an AWS account and get your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWs_BUCKET_NAME are in this [video](https://www.youtube.com/watch?v=JQVQcNN0cXE).

---
### Backend
1. Install virtualenv. 
    ```
    pip install virtualenv

    # or

    pip3 install virtualenv
    ```
    Virtualenv helps replicate exactly what will be on the server. This allows us to make sure our application is deployment ready and doesn't only work on our local machine.
2. Start virtualenv
    ```
    virtualenv <folder_name>

    # For example
    virtualenv venv
    ```
    This creates a python virtual enviornment.
3. Active the virtual environment
    ```
    # For Linux/Mac
    source venv/bin/activate

    # For Windows
    source venv/Scripts/activate
    ```
    You should see `(venv)` or whatever you named the python virtual enviornment when doing `step 2`
4.  Go into the backend directory and install requirements need to run the backend.
    ```
    cd backend

    pip install -r requirements.txt

    # or

    pip3 install -r requirements.txt
    ```
5. Create an `.env` file in `backend/backend/`. This will include all the secret information we need to run our backend.
    ```
    touch .env
    ```
    And add the following in the file
    ```
    # Django Settings
    SECRET_KEY = your_secret_key
    ENCRYPTION_KEY = your_encryption_key

    ## Database
    DATABASE_USERNAME=<user>
    DATABASE_PASSWORD=<password>
    DATABASE_HOST=<host>
    DATABASE_PORT=<port>
    DATABASE_NAME=<name>

    ## If using production database
    # DATABASE_URL=<database_url>

    # AWS S3
    AWS_ACCESS_KEY_ID = your_access_key_id
    AWS_SECRET_ACCESS_KEY = your_secret_access_key
    AWS_STORAGE_BUCKET_NAME = your_bucket_name


    # Email Service
    EMAIL_USERNAME = your_email_username
    EMAIL_PASS = your_email_password
    EMAIL_HOST = your_email_host
    EMAIL_PORT = your_email_port
    EMAIL_USE_TLS = your_email_use_tls

    # Links for Applications
    VERIFY_EMAIL_URL = your_verify_email_url
    RESET_PASSWORD_URL = your_reset_password_url

    # Geo Primary Key for session management
    Geo_Pimary_Key = your_geo_api_key
    ``` 