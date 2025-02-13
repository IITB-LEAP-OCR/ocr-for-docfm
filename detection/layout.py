from doclayout_yolo import YOLOv10
from doclayout_yolo.utils.ops import non_max_suppression
from huggingface_hub import hf_hub_download
import cv2
from tensorboard.util import io_util

filepath = hf_hub_download(repo_id="juliozhao/DocLayout-YOLO-DocStructBench", filename="doclayout_yolo_docstructbench_imgsz1024.pt")
model = YOLOv10(filepath)
# class_names = {0: 'title', 1: 'plain text', 2: 'abandon', 3: 'figure', 4: 'figure_caption', 5: 'table', 6: 'table_caption', 7: 'table_footnote', 8: 'isolate_formula', 9: 'formula_caption'}

def get_page_layout(image_path, layout_annotated_image_path, device = 'cpu'):
    det_res = model.predict(
    image_path,   # Image to predict
    imgsz = 1024,        # Prediction image size
    conf = 0.1,          # Confidence threshold
    iou = 0.0001,          # NMS Threshold
    device = device,    # Device to use (e.g., 'cuda:0' or 'cpu')
    save = False)
    dets = []
    for entry in det_res:
        bboxes = entry.boxes.xyxy.cpu().numpy()
        classes = entry.boxes.cls.cpu().numpy()
        # conf = entry.boxes.conf.cpu().numpy()
        for i in range(len(bboxes)):
            box = bboxes[i]
            dets.append([classes[i], [int(box[0]), int(box[1]), int(box[2]), int(box[3])]])

        annotated_frame = det_res[0].plot(pil=True, line_width=5, font_size=20)
        cv2.imwrite(layout_annotated_image_path, annotated_frame)
    return dets


