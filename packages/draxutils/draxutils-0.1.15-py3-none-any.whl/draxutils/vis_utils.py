import numpy as np
from PIL import Image
import torch
import cv2

def create_visualized_result(image, bbox=None, gt_mask=None, pred_mask=None):
    """
    Create a visualized result of an image with bounding box, ground truth mask, and predicted mask.

    Args:
    image (numpy.ndarray, PIL.Image.Image, or torch.Tensor): The original image.
        If numpy.ndarray or torch.Tensor, shape should be (H, W, 3) for RGB or (H, W, 4) for RGBA.
        If torch.Tensor, it should be on CPU and have dtype torch.uint8.
    bbox (tuple, optional): Bounding box coordinates (x, y, width, height).
        If None, it will be calculated from gt_mask or pred_mask.
    gt_mask (numpy.ndarray, PIL.Image.Image, or torch.Tensor, optional): Ground truth mask.
        If numpy.ndarray or torch.Tensor, shape should be (H, W) or (H, W, 1).
    pred_mask (numpy.ndarray, PIL.Image.Image, or torch.Tensor, optional): Predicted mask.
        If numpy.ndarray or torch.Tensor, shape should be (H, W) or (H, W, 1).

    Returns:
    numpy.ndarray: RGB image array with visualizations, shape (H, W, 3).

    The function overlays:
    - Red bounding box (calculated if not provided)
    - Blue semi-transparent ground truth mask (if provided)
    - Green semi-transparent predicted mask (if provided)
    """
    # Convert image to NumPy array if it's a PIL Image or PyTorch Tensor
    img_array = to_numpy(image)

    img_height, img_width = img_array.shape[:2]

    # Create a copy of the image for drawing
    result = img_array.copy()

    # Prepare masks
    gt_mask_array = prepare_mask(gt_mask, (img_width, img_height)) if gt_mask is not None else None
    pred_mask_array = prepare_mask(pred_mask, (img_width, img_height)) if pred_mask is not None else None

    # Calculate bbox if not provided
    if bbox is None:
        mask_for_bbox = gt_mask_array if gt_mask_array is not None else pred_mask_array
        if mask_for_bbox is not None:
            bbox = calculate_bbox(mask_for_bbox)

    # Draw bounding box using cv2
    if bbox is not None:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red box

    # Overlay ground truth mask
    if gt_mask_array is not None:
        gt_mask_colored = np.zeros((img_height, img_width, 3), dtype=np.uint8)
        gt_mask_colored[gt_mask_array > 0] = [255, 0, 0]  # Blue
        result = cv2.addWeighted(result, 1, gt_mask_colored, 0.5, 0)

    # Overlay predicted mask
    if pred_mask_array is not None:
        pred_mask_colored = np.zeros((img_height, img_width, 3), dtype=np.uint8)
        pred_mask_colored[pred_mask_array > 0] = [0, 255, 0]  # Green
        result = cv2.addWeighted(result, 1, pred_mask_colored, 0.5, 0)

    return result

def calculate_bbox(mask):
    """
    Calculate bounding box from a binary mask.

    Args:
    mask (numpy.ndarray): Binary mask, shape (H, W).

    Returns:
    tuple: Bounding box coordinates (x, y, width, height).
    """
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    y, y2 = np.where(rows)[0][[0, -1]]
    x, x2 = np.where(cols)[0][[0, -1]]
    return x, y, x2-x+1, y2-y+1

def prepare_mask(mask, target_size):
    """
    Prepare a mask for use in create_visualized_result.

    Args:
    mask (numpy.ndarray, PIL.Image.Image, or torch.Tensor): Input mask.
        If numpy.ndarray or torch.Tensor, shape should be (H, W) or (H, W, 1).
    target_size (tuple): Target size as (width, height).

    Returns:
    numpy.ndarray: Prepared mask array, shape (H, W).
    """
    mask_array = to_numpy(mask)

    if mask_array.shape[:2] != target_size[::-1]:
        return cv2.resize(mask_array.squeeze(), target_size, interpolation=cv2.INTER_NEAREST)
    return mask_array.squeeze()

def to_numpy(image):
    """
    Convert various image types to a NumPy array.

    Args:
    image (numpy.ndarray, PIL.Image.Image, or torch.Tensor): Input image.

    Returns:
    numpy.ndarray: Image as a NumPy array.
    """
    if isinstance(image, np.ndarray):
        return image
    elif isinstance(image, Image.Image):
        return np.array(image)
    elif isinstance(image, torch.Tensor):
        return image.cpu().numpy()
    else:
        raise ValueError("Input must be a NumPy array, PIL Image, or PyTorch Tensor")