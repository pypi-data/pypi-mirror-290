import os
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import cv2
from PIL import Image


def serialize_polygons(phenocam_rois):
    """
    Converts a dictionary of polygons to be YAML-friendly by converting tuples to lists.
    
    Parameters:
        phenocam_rois (dict of dict): Dictionary where keys are ROI names and values are dictionaries representing polygons.
    
    Returns:
        yaml_friendly_rois (dict of dict): Dictionary with tuples converted to lists.
    """
    yaml_friendly_rois = {}
    for roi, polygon in phenocam_rois.items():
        yaml_friendly_polygon = {
            'points': [list(point) for point in polygon['points']],
            'color': list(polygon['color']),
            'thickness': polygon['thickness']
        }
        yaml_friendly_rois[roi] = yaml_friendly_polygon
    return yaml_friendly_rois

def deserialize_polygons(yaml_friendly_rois):
    """
    Converts YAML-friendly polygons back to their original format with tuples.
    
    Parameters:
        yaml_friendly_rois (dict of dict): Dictionary where keys are ROI names and values are dictionaries representing polygons in YAML-friendly format.
    
    Returns:
        original_rois (dict of dict): Dictionary with points and color as tuples.
    """
    original_rois = {}
    for roi, polygon in yaml_friendly_rois.items():
        original_polygon = {
            'points': [tuple(point) for point in polygon['points']],
            'color': tuple(polygon['color']),
            'thickness': polygon['thickness']
        }
        original_rois[roi] = original_polygon
    return original_rois


def overlay_polygons(image_path, phenocam_rois: dict, show_names: bool = True, font_scale: float = 1.0):
    """
    Overlays polygons on an image and optionally labels them with their respective ROI names.

    Parameters:
        image_path (str): Path to the image file.
        phenocam_rois (dict): Dictionary where keys are ROI names and values are dictionaries representing polygons.
        Each dictionary should have the following keys:
        - 'points' (list of tuple): List of (x, y) tuples representing the vertices of the polygon.
        - 'color' (tuple): (B, G, R) color of the polygon border.
        - 'thickness' (int): Thickness of the polygon border.
        show_names (bool): Whether to display the ROI names on the image. Default is True.
        font_scale (float): Scale factor for the font size of the ROI names. Default is 1.0.

    Returns:
        numpy.ndarray: The image with polygons overlaid, in RGB format.
    """
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("Image not found or path is incorrect")
    
    for roi, polygon in phenocam_rois.items():
        # Extract points, color, and thickness from the polygon dictionary
        points = np.array(polygon['points'], dtype=np.int32)
        color = polygon['color']
        thickness = polygon['thickness']
        
        # Draw the polygon on the image
        cv2.polylines(img, [points], isClosed=True, color=color, thickness=thickness)
        
        if show_names:
            # Calculate the centroid of the polygon for labeling
            M = cv2.moments(points)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
            else:
                # In case of a degenerate polygon where area is zero
                cX, cY = points[0][0], points[0][1]
            
            # Overlay the ROI name at the centroid of the polygon
            cv2.putText(img, roi, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)

    # Convert the image from BGR to RGB before returning
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img_rgb

def compute_RGB_daily_average(records_list: List[Dict[str, Any]], products_dirpath: str, datatype_acronym: str = 'RGB', product_processing_level: str = 'L2_daily') -> Path:
    """
    Computes daily average RGB images from a list of records and saves them as .jpg files.

    Parameters:
        records_list (List[Dict[str, Any]]): List of dictionaries where each dictionary contains metadata and the image path.
        products_dirpath (str): Path to the directory where the processed images will be saved.
        datatype_acronym (str, optional): Acronym for the data type, default is 'RGB'.
        product_processing_level (str, optional): Processing level for the product, default is 'L2_daily'.

    Returns:
        Path: Path to the directory where the daily averaged images are saved.
    """
    images = []
    daily_image_catalog_guids = []

    for record in records_list:
        try:
            catalog_guid = record['catalog_guid']
            year = record['year']
            day_of_year = record['day_of_year']
            station_acronym = record['station_acronym']
            location_id = record['location_id']
            platform_id = record['platform_id']
            catalog_filepath = record['catalog_filepath']

            output_dirpath = Path(products_dirpath) / f'L2_{datatype_acronym}'  / str(year)

            if not os.path.exists(output_dirpath):
                os.makedirs(output_dirpath)

            img = cv2.imread(catalog_filepath)
            if img is not None:
                images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                daily_image_catalog_guids.append(catalog_guid)
            else:
                print(f"Warning: Unable to read image at {catalog_filepath}")
        except KeyError as e:
            print(f"Error: Missing key {e} in record {record}")
        except Exception as e:
            print(f"Unexpected error processing record {record}: {e}")

    if images:
        try:
            # Compute element-wise daily average
            avgImg = np.mean(images, axis=0)
            
            # Converting float64 type ndarray to uint8
            intImage = np.around(avgImg).astype(np.uint8)  # Round first and then convert to integer
            
            # Saving the daily average as image
            im = Image.fromarray(intImage)
            
            product_name = f'SITES-{station_acronym}-{location_id}-{platform_id}-{datatype_acronym}-{year}-DOY_{day_of_year}_{product_processing_level}.JPG'
            output_filepath = output_dirpath / product_name

            # Save image in the defined path
            im.save(output_filepath)
            print(f"Saved daily averaged image to {output_filepath}")
        except Exception as e:
            print(f"Error during image processing or saving: {e}")
    else:
        print("No images were processed. No output file created.")

    return output_filepath


def compute_GCC_RCC(daily_rgb_filepath: str, products_dirpath: str, year: int) -> dict:
    """
    Computes GCC and RCC images from a daily average RGB image and saves them as grayscale images.

    Parameters:
        daily_rgb_filepath (str): File path to the daily average RGB image.
        products_dirpath (str): Path to the directory where the processed images will be saved.
        year (int): Year for which the GCC and RCC images are being processed.

    Returns:
        dict: Dictionary containing file paths to the saved GCC and RCC images.
    """
    try:
        # Define directories to save GCC and RCC images
        gcc_dirpath = Path(products_dirpath) / 'L2_GCC'  / str(year)
        rcc_dirpath = Path(products_dirpath) / 'L2_RCC' / str(year)
        
        # Ensure the directories exist
        gcc_dirpath.mkdir(parents=True, exist_ok=True)
        rcc_dirpath.mkdir(parents=True, exist_ok=True)
        
        # Extracting image file name
        imgName = os.path.basename(daily_rgb_filepath)
        
        # Reading the RGB image
        cv_img = cv2.imread(daily_rgb_filepath)
        if cv_img is None:
            raise FileNotFoundError(f"Image file not found or unable to read: {daily_rgb_filepath}")
        
        # Extracting RGB bands as separate numpy arrays
        B = cv_img[:,:,0]
        G = cv_img[:,:,1]
        R = cv_img[:,:,2]

        # Element-wise addition of BGR array to calculate Total DN values in RGB band (i.e. R+G+B)
        DNtotal = cv_img.sum(axis=2)

        # Compute pixel-wise GCC and RCC from daily average images
        gcc = np.divide(G, DNtotal, out=np.zeros_like(G, dtype=float), where=DNtotal!=0)
        rcc = np.divide(R, DNtotal, out=np.zeros_like(R, dtype=float), where=DNtotal!=0)

        # Convert NaN to zero
        gcc = np.nan_to_num(gcc, copy=False)
        rcc = np.nan_to_num(rcc, copy=False)

        # Converting GCC and RCC to smoothly range from 0 - 255 as 'uint8' data type from 'float64'
        intImage1 = (gcc * 255).astype(np.uint8) 
        intImage2 = (rcc * 255).astype(np.uint8)

        # Convert to BGR format for saving
        cv_img_gcc = cv2.cvtColor(intImage1, cv2.COLOR_GRAY2BGR)
        cv_img_rcc = cv2.cvtColor(intImage2, cv2.COLOR_GRAY2BGR)

        # Define paths for saving images with given file names
        gcc_filepath = os.path.join(gcc_dirpath, imgName.replace('RGB', 'GCC'))
        rcc_filepath = os.path.join(rcc_dirpath, imgName.replace('RGB', 'RCC'))

        # Save images in the defined paths
        cv2.imwrite(gcc_filepath, cv_img_gcc)
        cv2.imwrite(rcc_filepath, cv_img_rcc)
        
        return {'gcc_filepath': gcc_filepath, 'rcc_filepath': rcc_filepath}

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing key {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}
    
def rois_mask_and_sum(image_path: str, phenocam_rois: dict) -> dict:
    """
    Masks an image based on the provided ROIs, calculates the sum of pixel values inside each ROI for R, G, and B channels,
    and returns a dictionary with the ROI name, sum of pixel values for each channel, and the number of summed pixels.

    Parameters:
        image_path (str): Path to the image file.
        phenocam_rois (dict): Dictionary where keys are ROI names and values are dictionaries representing polygons.
        Each dictionary should have the following keys:
        - 'points' (list of tuple): List of (x, y) tuples representing the vertices of the polygon.
        - 'color' (tuple): (B, G, R) color of the polygon border.
        - 'thickness' (int): Thickness of the polygon border.

    Returns:
        dict: A dictionary where each key is an ROI name, and the value is another dictionary containing:
              - 'sum_r': The sum of all pixel values inside the ROI mask for the red channel.
              - 'sum_g': The sum of all pixel values inside the ROI mask for the green channel.
              - 'sum_b': The sum of all pixel values inside the ROI mask for the blue channel.
              - 'num_pixels': The number of pixels that were summed inside the ROI.
              
    Example:
        ```python
        # Example usage
        if __name__ == "__main__":
            # Define the phenocam ROIs
            phenocam_rois = {
                'ROI_01': {
                    'points': [(100, 1800), (2700, 1550), (2500, 2700), (100, 2700)],
                    'color': (0, 255, 0),
                    'thickness': 7
                },
                'ROI_02': {
                    'points': [(100, 930), (3700, 1050), (3700, 1200), (100, 1400)],
                    'color': (0, 0, 255),
                    'thickness': 7
                },
                'ROI_03': {
                    'points': [(750, 600), (3700, 650), (3500, 950), (100, 830)],
                    'color': (255, 0, 0),
                    'thickness': 7
                }
            }
            
            # Apply the function to an image
            image_path = "path/to/your/image.jpg"
            roi_sums = rois_mask_and_sum(image_path, phenocam_rois)
        
        # >>>
                {
            'ROI_01': {
                'sum_r': 123456789,
                'sum_g': 987654321,
                'sum_b': 567890123,
                'num_pixels': 2553501
            },
            'ROI_02': {
                'sum_r': 112233445,
                'sum_g': 556677889,
                'sum_b': 223344556,
                'num_pixels': 1120071
            },
            'ROI_03': {
                'sum_r': 998877665,
                'sum_g': 554433221,
                'sum_b': 776655443,
                'num_pixels': 881151
            }
        }        
        ```
    """
    # Read the image as a color image (BGR format)
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("Image not found or path is incorrect")
    
    roi_sums = {}

    for roi, polygon in phenocam_rois.items():
        # Create a mask for the ROI
        mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Mask with the same height and width as the image
        points = np.array(polygon['points'], dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)
        
        # Apply the mask to each channel
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        
        # Calculate the sum of pixel values within the ROI for each channel
        sum_b = np.sum(masked_img[:, :, 0][mask == 255])
        sum_g = np.sum(masked_img[:, :, 1][mask == 255])
        sum_r = np.sum(masked_img[:, :, 2][mask == 255])
        num_pixels = np.sum(mask == 255)
        
        # Store the results in the dictionary
        roi_sums[roi] = {
            'SUM_Red': int(sum_r),
            'SUM_Green': int(sum_g),
            'SUM_Blue': int(sum_b),
            'num_pixels': int(num_pixels)
        }

    return roi_sums    

def convert_rois_sums_to_single_dict(rois_sums_dict):
    """
    Converts the rois_sums_dict into a single dictionary with keys in the format 'L2_<ROI_NAME>_<suffix>'.

    The `rois_sums_dict` is expected to contain sums of pixel values for each color channel (R, G, B) and the number of pixels
    within each ROI, as calculated by the `rois_mask_and_sum` function.

    Parameters:
        rois_sums_dict (dict): A dictionary where keys are ROI names and values are dictionaries containing:
                               - 'sum_r': The sum of all pixel values inside the ROI mask for the red channel.
                               - 'sum_g': The sum of all pixel values inside the ROI mask for the green channel.
                               - 'sum_b': The sum of all pixel values inside the ROI mask for the blue channel.
                               - 'num_pixels': The number of pixels that were summed inside the ROI.

    Returns:
        dict: A single dictionary containing the combined key-value pairs in the format:
              - 'L2_<ROI_NAME>_sum_r': Sum of pixel values for the red channel in the ROI.
              - 'L2_<ROI_NAME>_sum_g': Sum of pixel values for the green channel in the ROI.
              - 'L2_<ROI_NAME>_sum_b': Sum of pixel values for the blue channel in the ROI.
              - 'L2_<ROI_NAME>_num_pixels': Number of pixels summed in the ROI.
              
    Example:
        ```python
        
        rois_sums_dict = {
            'ROI_01': {
                'sum_r': 123456789,
                'sum_g': 987654321,
                'sum_b': 567890123,
                'num_pixels': 2553501
            },
            'ROI_02': {
                'sum_r': 112233445,
                'sum_g': 556677889,
                'sum_b': 223344556,
                'num_pixels': 1120071
            },
            'ROI_03': {
                'sum_r': 998877665,
                'sum_g': 554433221,
                'sum_b': 776655443,
                'num_pixels': 881151
            }
        }

        # Create a single dictionary
        single_dict = convert_rois_sums_to_single_dict(rois_sums_dict)

        print(single_dict)
                
        # Output:
        
            {
            'L2_ROI_01_sum_r': 123456789,
            'L2_ROI_01_sum_g': 987654321,
            'L2_ROI_01_sum_b': 567890123,
            'L2_ROI_01_num_pixels': 2553501,
            'L2_ROI_02_sum_r': 112233445,
            'L2_ROI_02_sum_g': 556677889,
            'L2_ROI_02_sum_b': 223344556,
            'L2_ROI_02_num_pixels': 1120071,
            'L2_ROI_03_sum_r': 998877665,
            'L2_ROI_03_sum_g': 554433221,
            'L2_ROI_03_sum_b': 776655443,
            'L2_ROI_03_num_pixels': 881151
        }
        ```
    """
    # Initialize an empty dictionary
    combined_dict = {}

    # Iterate over the rois_sums_dict to create the single dictionary
    for roi_name, metrics in rois_sums_dict.items():
        for suffix, value in metrics.items():
            combined_dict[f'L2_{roi_name}_{suffix}'] = value

    return combined_dict