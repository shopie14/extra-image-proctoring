import json
import os
import requests
from urllib.parse import urlparse
import time
from datetime import datetime

def download_image(image_url, folder_path):
    image_name = os.path.basename(urlparse(image_url).path)
    image_path = os.path.join(folder_path, image_name)

    # Skip download if the file already exists
    if os.path.exists(image_path):
        print(f"Skipping download for {image_url} - File already exists.")
        return image_path

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)
        print(f"Downloaded: {image_url}")
        return image_path
    else:
        print(f"Failed to download image from {image_url}")
        return None

def is_year_2024(timestamp):
    # Convert Unix timestamp (milliseconds) to datetime
    timestamp = int(timestamp) / 1000  # Convert to seconds
    date_time = datetime.utcfromtimestamp(timestamp)
    return date_time.year == 2024

def organize_images(images):
    start_time = time.time()
    total_images = 0
    for entry in images:
        image_url = entry['image_url']
        image_name = os.path.basename(urlparse(image_url).path)
       
        try:
            timestamp = image_name.split('-')[-1].split('.')[0]  
            if is_year_2024(timestamp):
                folder_path = "E:/KAMPUS/LMS PPTIK/Get Image Proctoring Maret 2024/vr_proctoring"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                downloaded_image_path = download_image(image_url, folder_path)
                if downloaded_image_path:
                    total_images += 1
        except (IndexError, ValueError):
            print(f"Invalid file name format or timestamp: {image_name}")
            continue

    end_time = time.time()
    duration = end_time - start_time
    summary = {
        "Total_Images_Downloaded": total_images,
        "Duration_Seconds": duration
    }

    print("\nSummary:")
    print(json.dumps(summary, indent=2))

    # Save the summary to a JSON file
    with open("summary.json", "w") as json_file:
        json.dump(summary, json_file, indent=2)

if __name__ == "__main__":
    # Load your images data here
    with open("engagement.vr_proctoring.json", "r") as file:
        engagement_data = json.load(file)

    # Extract image data from the engagement data
    face_data = [entry for entry in engagement_data if 'image_url' in entry]

    # Organize and download images
    organize_images(face_data)
