from services_api.seg_and_track import Roi, Mask

def to_roi_msg(roi):
    return Roi(
        x=int(roi[1].start),
        y=int(roi[0].start),
        width=int(roi[1].stop - roi[1].start),
        height=int(roi[0].stop - roi[0].start),
    )


def to_mask_msg(mask_in_roi, roi, width, height):
    return Mask(width=width, height=height, roi=to_roi_msg(roi), mask_in_roi=mask_in_roi.flatten().tolist())
