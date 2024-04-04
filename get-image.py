import json
import os
import requests
from urllib.parse import urlparse
import time

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
        return image_path
    else:
        print(f"Failed to download image from {image_url}")
        return None

def organize_images(images):
    start_time = time.time()
    
    total_images = 0
    unique_usernames = set()

    for entry in images:
        username = entry['username']
        image_url = entry['image_url']
        folder_path = os.path.join("E:/KAMPUS/LMS PPTIK/Get Image Proctoring Maret 2024/data")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        downloaded_image_path = download_image(image_url, folder_path)

        if downloaded_image_path:
            print(f"Downloaded image for {username}: {downloaded_image_path}")
            total_images += 1
            unique_usernames.add(username)

    end_time = time.time()
    duration = end_time - start_time

    summary = {
        "Total_Images_Downloaded": total_images,
        "Total_Unique_Usernames": len(unique_usernames),
        "Duration_Seconds": duration
    }

    print("\nSummary:")
    print(json.dumps(summary, indent=2))

    # Save the summary to a JSON file
    with open("summary.json", "w") as json_file:
        json.dump(summary, json_file, indent=2)

if __name__ == "__main__":
    # Read data from engagement.proctoring.json
    with open("engagement.logproctorings4.json", "r") as file:
        engagement_data = json.load(file)

    # Extract image data from the engagement data
    face_data = [entry for entry in engagement_data if 'image_url' in entry]

    # Organize and download images
    organize_images(face_data)