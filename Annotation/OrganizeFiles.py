import os
import shutil

Year = 1941

# Paths
google_drive_path = 'G:/My Drive/Tokyo_Jobs/'+str(Year)
local_base_path = 'C:/Users/' + User + '/Box/Research Notes (keitaro2@illinois.edu)/Tokyo_Jobs/Processed_Data/'+str(Year)

if not os.path.exists(google_drive_path):
    os.makedirs(google_drive_path)

# Iterate through folders in Google Drive path
for folder_name in os.listdir(local_base_path):
    if folder_name.startswith("Page"):
        page_folder_path = os.path.join(google_drive_path, folder_name, "output")
        if os.path.isdir(page_folder_path):
            # Assuming only one subfolder exists inside the "output" folder
            output_subfolders = os.listdir(page_folder_path)
            if output_subfolders:
                random_folder_name = output_subfolders[0]
                json_folder_path = os.path.join(page_folder_path, random_folder_name, "json")
                
                if os.path.isdir(json_folder_path):
                    # Define local destination path
                    local_dest_path = os.path.join(local_base_path, folder_name, "NDLoutput")
                    os.makedirs(local_dest_path, exist_ok=True)

                    # Copy files from json folder to local destination
                    for file_name in os.listdir(json_folder_path):
                        source_file = os.path.join(json_folder_path, file_name)
                        dest_file = os.path.join(local_dest_path, file_name)
                        shutil.copy(source_file, dest_file)

print("Files copied successfully.")

