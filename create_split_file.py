import os
import glob
import random
import argparse

# Argument parser setup
parser = argparse.ArgumentParser(description="Split dataset into train and validation sets")
parser.add_argument('--data_path', type=str, required=True, help='Path to dataset')
parser.add_argument('--save_path', type=str, required=True, help='Path to save txt files')
parser.add_argument('--split_ratio', type=str, default="9:1", help='Split ratio for train:val')
args = parser.parse_args()

# Parsing the split ratio
a, b = map(int, args.split_ratio.split(":"))
split_ratio = a / (a + b)

# Ensure save directory exists
os.makedirs(args.save_path, exist_ok=True)

# Paths for the output txt files
train_file_path = os.path.join(args.save_path, "train_files.txt")
val_file_path = os.path.join(args.save_path, "val_files.txt")

# Collecting all image paths
all_file_list = []
date_folders = os.listdir(args.data_path)
os.chdir(args.data_path)  # Change working directory to the dataset pat
for df in date_folders:
    if os.path.isdir(df):
        # Gather all image files in the folder
        images = sorted(glob.glob(os.path.join(df, "*.jpg")))
        
        # Exclude first and last images
        if len(images) > 2:  # Ensure there are enough images to exclude
            images = images[1:-1]

        for image in images:
            image_name = os.path.basename(image).replace(".jpg", "")  # Remove .jpg extension
            all_file_list.append(f"{df} {image_name} l\n")


# Shuffle and split the dataset
random.shuffle(all_file_list)
split_index = int(len(all_file_list) * split_ratio)

train_files = all_file_list[:split_index]
val_files = all_file_list[split_index:]

# Save to train_files.txt and val_files.txt
with open(train_file_path, 'w') as train_file:
    train_file.writelines(train_files)

with open(val_file_path, 'w') as val_file:
    val_file.writelines(val_files)

print(f"Train file saved to: {train_file_path}")
print(f"Validation file saved to: {val_file_path}")