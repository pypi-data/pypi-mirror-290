import math

def check_distance_within(source, distination, radius):
    cust_lat, cust_long = source
    central_lat, central_long = distination
    
    # Convert latitude and longitude from degrees to radians
    central_lat_rad = math.radians(central_lat)
    central_long_rad = math.radians(central_long)
    cust_lat_rad = math.radians(cust_lat)
    cust_long_rad = math.radians(cust_long)
    
    # Haversine formula
    delta_lat = cust_lat_rad - central_lat_rad
    delta_long = cust_long_rad - central_long_rad
    
    a = math.sin(delta_lat / 2)**2 + math.cos(central_lat_rad) * math.cos(cust_lat_rad) * math.sin(delta_long / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    
    # Check if the customer location falls within the specified range
    if distance <= int(radius):
        return {'status':200, 'message':"valid", "distance":distance }
    else:
        return {'status':400, 'message':"invalid", "distance":distance }
    
def get_distance(source, distination):
    cust_lat, cust_long = source
    central_lat, central_long = distination
    
    # Convert latitude and longitude from degrees to radians
    central_lat_rad = math.radians(central_lat)
    central_long_rad = math.radians(central_long)
    cust_lat_rad = math.radians(cust_lat)
    cust_long_rad = math.radians(cust_long)
    
    # Haversine formula
    delta_lat = cust_lat_rad - central_lat_rad
    delta_long = cust_long_rad - central_long_rad
    
    a = math.sin(delta_lat / 2)**2 + math.cos(central_lat_rad) * math.cos(cust_lat_rad) * math.sin(delta_long / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    
    # Check if the customer location falls within the specified range
    if distance:
        return distance
    else:
        return {'status':400, 'message':"invalid" }