import json
from datetime import datetime, timedelta, timezone
import os
import glob
import math

def parse_gps(gps_str):
    """Convert GPS string (e.g., 'N42.389457 W72.526538') to decimal degrees."""
    lat_str, lon_str = gps_str.split()
    lat_dir = lat_str[0]
    lat = float(lat_str[1:])
    if lat_dir in ('S', 's'):
        lat = -lat
    lon_dir = lon_str[0]
    lon = float(lon_str[1:])
    if lon_dir in ('W', 'w'):
        lon = -lon
    return lat, lon

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance in meters between two points."""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def parse_files(directory):
    """Parse all .json/.vtt file pairs and extract timestamped GPS data."""
    officers_data = {}
    
    # Search recursively for JSON files
    for json_path in glob.glob(os.path.join(directory, '**/*.json'), recursive=True):
        base_name = os.path.splitext(json_path)[0]
        vtt_path = base_name + '.vtt'
        
        if not os.path.exists(vtt_path):
            continue
            
        # Parse JSON timestamps
        try:
            with open(json_path, 'r') as f:
                json_content = json.load(f)
            timestamps = []
            for dp in json_content.get('DataPoints', []):
                time_str = dp.get('Time')
                if time_str:
                    try:
                        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                        timestamps.append(dt)
                    except ValueError:
                        pass
        except Exception as e:
            continue
            
        # Parse VTT GPS data
        try:
            with open(vtt_path, 'r') as f:
                content = f.read()
            sections = content.split('\n\n')
            gps_entries = []
            officer_name = None
            for section in sections:
                lines = section.strip().split('\n')
                if len(lines) < 2:
                    continue
                try:
                    data = json.loads('\n'.join(lines[1:]))
                    gps_str = data.get('gpsCoordinates')
                    officer = data.get('officer')
                    if not gps_str or not officer:
                        continue
                    if not officer_name:
                        officer_name = officer
                    elif officer != officer_name:
                        continue
                    lat, lon = parse_gps(gps_str)
                    gps_entries.append((lat, lon))
                except Exception as e:
                    continue
        except Exception as e:
            continue
            
        # Pair timestamps with GPS data
        min_length = min(len(timestamps), len(gps_entries))
        if officer_name and min_length > 0:
            if officer_name not in officers_data:
                officers_data[officer_name] = []
            for i in range(min_length):
                officers_data[officer_name].append((timestamps[i], gps_entries[i][0], gps_entries[i][1]))
    
    # Sort entries by time for each officer
    for officer in officers_data:
        officers_data[officer].sort(key=lambda x: x[0])
    
    return officers_data

def find_officers_at_time(officers_data, target_time, threshold_seconds=1):
    """Find officers' positions closest to the target time within threshold."""
    try:
        # Ensure target_dt is offset-aware (UTC)
        target_dt = datetime.fromisoformat(target_time.replace('Z', '+00:00'))
    except ValueError:
        return {}
    
    results = {}
    for officer, entries in officers_data.items():
        closest = None
        min_diff = float('inf')
        for ts, lat, lon in entries:
            # Ensure ts is offset-aware (UTC)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            diff = abs((ts - target_dt).total_seconds())
            if diff < min_diff:
                min_diff = diff
                closest = (lat, lon)
        if closest is not None and min_diff <= threshold_seconds:
            results[officer] = closest
    return results

def find_proximity_to_officer(officers, target_officer, max_distance=100):
    """Find officers within max_distance meters of the target officer."""
    proximate = []
    if target_officer not in officers:
        return proximate
    
    target_lat, target_lon = officers[target_officer]
    for name, (lat, lon) in officers.items():
        if name == target_officer:
            continue
        distance = haversine(target_lat, target_lon, lat, lon)
        if distance <= max_distance:
            proximate.append((name, distance))
    
    # Sort by distance
    proximate.sort(key=lambda x: x[1])
    return proximate

def main():
    directory = input("Enter directory containing .json/.vtt files: ").strip()
    target_time = input("Enter target timestamp (ISO 8601 format, e.g., 2024-05-08T02:04:14.016256Z): ").strip()
    target_officer = input("Enter officer name to check proximity to: ").strip()
    
    max_dist_input = input("Maximum proximity distance in meters [100]: ").strip()
    max_distance = 100
    if max_dist_input:
        try:
            max_distance = float(max_dist_input)
        except ValueError:
            print("Invalid distance input. Using default 100 meters.")
    
    print("\nProcessing files...")
    officers_data = parse_files(directory)
    
    if not officers_data:
        print("No valid officer data found.")
        return
    
    officers_at_time = find_officers_at_time(officers_data, target_time)
    
    if target_officer not in officers_at_time:
        print(f"\nOfficer '{target_officer}' not found at {target_time}.")
        return
    
    proximate = find_proximity_to_officer(officers_at_time, target_officer, max_distance)
    
    print(f"\nResults for {target_time}:")
    print(f"Target officer: {target_officer}")
    print(f"Maximum proximity: {max_distance} meters\n")
    
    if not proximate:
        print("No other officers were within proximity.")
    else:
        print("Nearby officers:")
        for name, distance in proximate:
            print(f" - {name}: {distance:.2f} meters away")

if __name__ == '__main__':
    main()
