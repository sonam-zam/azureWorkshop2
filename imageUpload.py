import os
import time
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials
from concurrent.futures import ThreadPoolExecutor

# Set your Custom Vision API credentials and endpoint
credentials = ApiKeyCredentials(in_headers={"Training-key": "00e15d939583442eaedae66af2523e92"})
trainer = CustomVisionTrainingClient("https://azurepoc1.cognitiveservices.azure.com/", credentials)

imagenet_train_path = "C:\\Users\\Sonam\\Downloads\\cloud_ai_services_tutorial-main\\cloud_ai_services_tutorial-main\\Dataset\\imagenet5\\train"


# Function to upload and tag images for a given tag
def upload_and_tag_images(project, tag_name, class_folder):
    print(f"Uploading and tagging images for class: {tag_name}")
    tag_obj = trainer.create_tag(project.id, tag_name)

    for image_name in os.listdir(class_folder):
        image_path = os.path.join(class_folder, image_name)
        with open(image_path, "rb") as image_contents:
            retry_count = 0
            while retry_count < 3:  # Maximum retry attempts
                try:
                    trainer.create_images_from_data(project.id, image_contents.read(), [tag_obj.id])
                    print(f"Image {image_name} uploaded successfully.")
                    break  # Break the loop if the operation succeeds
                except Exception as e:
                    print(f"Error uploading image {image_name}: {e}")
                    if "Too Many Requests" in str(e):
                        print(f"Rate limit exceeded. Retrying after 60 seconds...")
                        time.sleep(60)
                        retry_count += 1
                    else:
                        raise  # Re-raise other exceptions

# Read labels from the file

# Batch size (adjust based on your project)
batch_size = 100

# Create a new project for each batch of labels
for i in range(0, len(labels), batch_size):
    batch_labels = labels[i:i + batch_size]
    
    # Introduce delay before creating a project
    time.sleep(5)
    
    try:
        batch_project = trainer.create_project(f"Batch_{i}")
    except Exception as e:
        print(f"Error creating project for batch {i}: {e}")
        continue

    with ThreadPoolExecutor() as executor:
        executor.map(upload_and_tag_images, [batch_project] * len(batch_labels), batch_labels, [imagenet_train_path] * len(batch_labels))

print("Image upload completed.")
