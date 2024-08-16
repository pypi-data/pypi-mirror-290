from PIL import Image as PILImage
from PIL import ImageDraw
import numpy as np

def create_visualized_result(image, bbox, gt_mask, pred_mask):
    img_width, img_height = image.size
    x, y, w, h = bbox
    x2, y2 = x + w, y + h

    result_image = image.copy().convert('RGBA')
    if bbox is not None:
        draw = ImageDraw.Draw(result_image)
        # Draw the bounding box
        draw.rectangle([x, y, x2, y2], outline="red", width=2)

    # Overlay the ground truth mask (blue)
    if gt_mask is not None:
        gt_mask = gt_mask.resize(image.size, PILImage.NEAREST)
        gt_mask_array = np.array(gt_mask)
        gt_colored_mask = np.zeros((img_height, img_width, 4), dtype=np.uint8)
        gt_colored_mask[gt_mask_array > 0] = [0, 0, 255, 64]  # Semi-transparent blue
        gt_mask_image = PILImage.fromarray(gt_colored_mask, mode='RGBA')
        result_image = PILImage.alpha_composite(result_image, gt_mask_image)

    # Overlay the predicted mask (green)
    if pred_mask is not None:
        pred_mask = pred_mask.resize(image.size, PILImage.NEAREST)
        pred_mask_array = np.array(pred_mask)
        pred_colored_mask = np.zeros((img_height, img_width, 4), dtype=np.uint8)
        pred_colored_mask[pred_mask_array > 0] = [0, 255, 0, 64]  # Semi-transparent green
        pred_mask_image = PILImage.fromarray(pred_colored_mask, mode='RGBA')
        result_image = PILImage.alpha_composite(result_image, pred_mask_image)

    return result_image.convert('RGB')