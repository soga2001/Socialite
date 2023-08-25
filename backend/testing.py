import geoip2.database

# Path to your .mmdb database file
mmdb_file_path = "geip/GeoLite2-City.mmdb"

# IP address you want to look up
target_ip = "8.8.8.8"

# Open the database file
with geoip2.database.Reader(mmdb_file_path) as reader:
    try:
        # Perform the IP lookup
        response = reader.city(target_ip)

        # Extract and print relevant information
        print("IP Address:", target_ip)
        print("Country:", response.country.name)
        print("City:", response.city.name)
        print("Latitude:", response.location.latitude)
        print("Longitude:", response.location.longitude)
        # Add more fields as needed
    except geoip2.errors.AddressNotFoundError:
        print("IP address not found in the database.")
