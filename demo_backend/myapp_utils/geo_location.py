from geopy.geocoders import Nominatim

def reverse_geocode(lat, lng):
    try:
        geolocator = Nominatim(user_agent="gas_scan")
        location = geolocator.reverse(f"{lat}, {lng}")
        print(location)
        return location.address if location else None
    except:
        return None
