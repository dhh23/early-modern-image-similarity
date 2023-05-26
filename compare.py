from PIL import Image
import os
from os import listdir
from pathlib import Path
import imagehash
import numpy as np

# Count duplicates just to be sure
duplicates = 0
# Get all images from the current directory fro the folder called "sample" and file extensions does not matter ("*")
images = Path("sample").glob('*')
# Datastructures for different objects for later processing
# List of images
image_list = []
# List of hashes of the images
hashes_list = []
# List of dictionaries, where the key is the hash of the image, and the value is the name of the image file
hash_image_list = []
# List of hashes of the images, which are similar or close to being similar
similar_pics_hash_list = []

for image in images:
    image_list.append(image)
    # Using average hash, other hash types could be tried for better accuracy
    hashes_list.append(imagehash.average_hash(Image.open(image)))
    entry = {"hash" : imagehash.average_hash(Image.open(image)), "image_file_name" : image}
    hash_image_list.append(entry)

# This cutoff value determines the similarity. Smaller for more accurate similarity, larger for not so accurate
cutoff_value = 3

# Go through the hashes of the images and compare them to each other to find the similar images
iterable = iter(hashes_list)
prev = next(iterable)
for element in iterable:
    diff = element - prev
    if diff < cutoff_value:
        duplicates = duplicates + 1
        similar_pics_hash_list.append(element)
        similar_pics_hash_list.append(prev)
        print("Difference between hashes: " + str(diff))
    prev = element

# Print just for fun and to confirm
print("Duplicates: " + str(duplicates))

image_names = []
# Show the similar images
# Check the images by the hashes, which were determined as similar / close to each other
for similar_hash in similar_pics_hash_list:
    for entry in hash_image_list:
        if entry["hash"] == similar_hash:
            image_names.append(entry["image_file_name"])
            # This opens the image in the computer's default viewing app
            # A bit of a lazy way, should be refactored to some better
            # For example show the duplicate images side by side
            im = Image.open(entry["image_file_name"], mode='r')
            im.show()

# List the file names of the similar images for manual inspection / confirmation
for name in image_names:
    print(name)