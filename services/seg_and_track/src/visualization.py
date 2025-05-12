import numpy as np
import cv2


def _check_label_fitness(image_size, text_size, text_pos):
    image_width, image_height = image_size
    text_width, text_height = text_size
    text_x, text_y = text_pos

    dx = 0
    if text_x < 0:
        dx = -text_x
    elif text_x + text_width > image_width:
        dx = image_width - text_x - text_width

    dy = 0
    if text_y < 0:
        dy = -text_y
    elif text_y + text_height > image_height:
        dy = image_height - text_y - text_height
    return dx, dy


def draw_objects(
    image,
    scores=None,
    objects_ids=None,
    boxes=None,
    masks=None,
    customs=None,
    min_score=0.0,
    draw_scores=False,
    draw_ids=False,
    draw_boxes=False,
    draw_masks=False,
    format_=None,
    palette=((0, 0, 255), (255, 0, 0)),
    color_by_object_id=False,
    color_by_class_id=True,
):
    if boxes is None and masks is None:
        raise RuntimeError("Both boxes and masks are None")
    if color_by_object_id and objects_ids is None:
        raise RuntimeError("color_by_object_id is set True, but objects_ids is None")

    if format_ is None:
        assert not draw_scores or scores is not None
        assert not draw_ids or objects_ids is not None
    assert not draw_boxes or boxes is not None
    assert not draw_masks or masks is not None

    num = None
    if scores is not None:
        assert num is None or len(scores) == num
        num = len(scores)
    if objects_ids is not None:
        assert num is None or len(objects_ids) == num
        num = len(objects_ids)
    if boxes is not None:
        assert num is None or len(boxes) == num
        num = len(boxes)
    if masks is not None:
        assert num is None or len(masks) == num
        num = len(masks)
    if customs is not None:
        assert num is None or len(customs) == num
        num = len(customs)

    if scores is None:
        scores = [None] * num
    if objects_ids is None:
        objects_ids = [None] * num
    if boxes is None:
        boxes = [None] * num
    if masks is None:
        masks = [None] * num
    if customs is None:
        customs = [None] * num

    if format_ is None:
        fields = []
        if draw_scores:
            fields.append("{s:.02f}")
        if draw_ids:
            fields.append("id: {i}")
        format_ = ", ".join(fields)

    width = image.shape[1]
    height = image.shape[0]
    overlay = image.copy()
    for i, (score, object_id, box, mask, custom) in enumerate(zip(scores, objects_ids, boxes, masks, customs)):
        if score is not None and score < min_score:
            continue

        if color_by_object_id:
            color = palette[object_id % len(palette)]
        elif color_by_class_id:
            color = palette[custom % len(palette)]
        else:
            color = palette[i % len(palette)]

        if format_:
            text = format_.format(s=score, i=object_id, c=custom)
            if box is not None:
                x, y_top, y_bottom = box[0], box[1], box[3]
            else:
                nonzero_y, nonzero_x = np.nonzero(mask)
                x, y_top, y_bottom = (nonzero_x.min(), nonzero_y.min(), nonzero_y.max())
            y = y_top - 5
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
            dx, dy = _check_label_fitness((width, height), text_size, (x, y))
            x += dx
            if dy > 0:
                y = y_bottom + text_size[1] + 5
            cv2.putText(image, text, (x, y), font, font_scale, color, thickness=thickness)

        if draw_boxes:
            x1, y1, x2, y2 = box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness=2)

        if draw_masks:
            overlay[mask != 0] = np.array(color, dtype=np.uint8)
            if not draw_boxes:
                polygons, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                cv2.polylines(image, polygons, True, color, thickness=2)

    cv2.addWeighted(image, 0.7, overlay, 0.3, 0, dst=image)

    return image
