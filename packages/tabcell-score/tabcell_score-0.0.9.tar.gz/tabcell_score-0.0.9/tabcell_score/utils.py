# Writer: TraiPPN2 # Date: 19/01/2024

import json
import numpy as np
import cv2


def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Calculate the intersection area
    x_intersection = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    y_intersection = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    intersection_area = x_intersection * y_intersection

    # Calculate the union area
    union_area = (w1 * h1) + (w2 * h2) - intersection_area

    # Avoid division by zero
    if union_area == 0:
        return 0.0

    # Calculate IoU
    iou = intersection_area / union_area

    return iou


def gen_blank_image(bboxes):
    height = int(max([x[3] for x in bboxes])) + int(min([x[1] for x in bboxes]))
    width = int(max([x[2] for x in bboxes])) + int(min([x[0] for x in bboxes]))
    return np.ones((height, width, 3), np.uint8) * 255


def load_label_from_file(path):
    # load cell bbox from labelme json
    with open(path, 'r') as file:
        data = json.load(file)
    return [x['points'][0] + x['points'][1] for x in data['shapes']]


def visualize(image, pred_boxes, 
              map_gt_pred,
              save_path,
              true_box_color = (0, 128, 0),
              false_box_color = (0, 0, 255)):
    
    boxes = np.array(pred_boxes, dtype=int)
    img = image.copy()

    for i, (x1, y1, x2, y2) in enumerate(boxes):
        if i in map_gt_pred:
            cv2.rectangle(img, (x1, y1), (x2, y2), true_box_color, 4)
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), false_box_color, 4)

    cv2.imwrite(save_path, img)