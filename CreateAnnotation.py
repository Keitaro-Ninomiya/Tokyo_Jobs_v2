import os, re
import json
from PIL import Image, ImageDraw

def get_ocr_file_path(image_location, base_folder, year, page):
    # Ensure the image_location is valid
    if image_location not in ocr_files:
        raise ValueError(f"Invalid image location: {image_location}")

    # Get the OCR file name for the given image location
    ocr_file_name = ocr_files[image_location]

    # Construct the full file path for the OCR output
    ocr_file_path = os.path.join(
        base_folder, f'Tokyo_Jobs/Processed_Data/{year}/Page{page:03d}/NDLoutput', ocr_file_name
    )
    return ocr_file_path

def get_page_range(base_folder, year):
    # Construct the path to the year directory
    year_path = os.path.join(base_folder, f'Tokyo_Jobs/Processed_Data/{year}')
    
    # Get a list of all items in the year directory
    try:
        items = os.listdir(year_path)
    except FileNotFoundError:
        print(f"The directory {year_path} does not exist.")
        return None, None

    # Filter out directories with the format "Page###"
    page_dirs = [item for item in items if re.match(r'Page\d+', item)]

    # Extract page numbers from the directory names
    page_numbers = [int(re.search(r'(\d+)', page_dir).group()) for page_dir in page_dirs if re.search(r'(\d+)', page_dir)]

    if page_numbers:
        # Determine the starting and ending page numbers
        start_page = min(page_numbers)
        end_page = max(page_numbers)
        return start_page, end_page
    else:
        print(f"No valid Page### directories found in {year_path}.")
        return None, None

# Function to build text to coordinate mapping
def build_text_to_coord(ocr_data):
    text_to_coord = {}
    for entry in ocr_data:
        if len(entry) == 5:
            x_min, y_min, x_max, y_max, text = entry
            text_to_coord[text] = (x_min, y_min, x_max, y_max)
    return text_to_coord

# Function to group entries into columns based on x-coordinates
def group_into_columns(ocr_data, column_threshold=15):
    text_to_coord = build_text_to_coord(ocr_data)
    columns = {}

    for text, (x_min, y_min, x_max, y_max) in text_to_coord.items():
        column_found = False

        for col_x in columns:
            if abs(col_x - x_min) <= column_threshold:
                columns[col_x]["entries"].append(text)
                columns[col_x]["bbox"] = [
                    [min(columns[col_x]["bbox"][0][0], x_min), min(columns[col_x]["bbox"][0][1], y_min)],
                    [max(columns[col_x]["bbox"][1][0], x_max), max(columns[col_x]["bbox"][1][1], y_max)]
                ]
                column_found = True
                break

        if not column_found:
            columns[x_min] = {"entries": [text], "bbox": [[x_min, y_min], [x_max, y_max]]}

    return columns

# Function to draw bounding boxes on an image
def draw_bounding_boxes_on_image(image_path, columns):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)

        for col_x, column_data in columns.items():
            bbox = column_data['bbox']
            entries = column_data['entries']
            bbox_flat = (bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
            
            # Draw the rectangle
            draw.rectangle(bbox_flat, outline="red", width=2)

            # Place text at the top-left corner of the bounding box
            for entry in entries:
                if entry in text_to_coord:
                    draw.text((bbox[0][0], bbox[0][1]), entry, fill="blue")

        # Define the save path with the "Annotated" prefix
        annotated_image_path = os.path.join(
            os.path.dirname(image_path), 
            'Annotated' + os.path.basename(image_path)
        )
        
        # Save the annotated image
        img.save(annotated_image_path)
        print(f"Annotated image saved at: {annotated_image_path}")

# Function to save bounding boxes as JSON for later annotation
def save_bounding_boxes_as_json(columns, save_path):
    # Prepare data for JSON serialization
    bbox_data = {}
    for col_x, column_data in columns.items():
        bbox = column_data['bbox']
        entries = column_data['entries']
        bbox_data[f"Column_{col_x}"] = {
            "entries": entries,
            "bounding_box": {
                "top_left": bbox[0],
                "bottom_right": bbox[1]
            }
        }

    # Write the data to a JSON file
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(bbox_data, file, indent=4)
    print(f"Bounding box data saved at: {save_path}")
    