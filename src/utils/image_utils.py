import sys
from PIL import Image, ImageDraw, ImageOps


def merge_images_horizontally(list_of_image_paths):
    images = [Image.open(x) for x in list_of_image_paths]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im


def merge_images_vertically(list_of_images):
    images = list_of_images
    widths, heights = zip(*(i.size for i in images))

    total_height = sum(heights)
    max_width = max(widths)

    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]

    return new_im


def draw_annotation_box_onto_image(image_to_draw_on, image_patch_metadata_object_containing_annotation_box_values,
                                   draw_border):
    TINT_COLOR = (0, 255, 0)  # Green
    TRANSPARENCY = .20  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', image_to_draw_on.size, TINT_COLOR + (0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    draw.rectangle(((image_patch_metadata_object_containing_annotation_box_values.x_coordinate,
                     image_patch_metadata_object_containing_annotation_box_values.y_coordinate),
                    (
                        image_patch_metadata_object_containing_annotation_box_values.x_coordinate + image_patch_metadata_object_containing_annotation_box_values.width,
                        image_patch_metadata_object_containing_annotation_box_values.y_coordinate + image_patch_metadata_object_containing_annotation_box_values.height)),
                   fill=TINT_COLOR + (OPACITY,), outline="black" if draw_border else None, width=4 if draw_border else 0)

    image_with_annotation_box = Image.alpha_composite(image_to_draw_on, overlay)
    image_with_annotation_box = image_with_annotation_box.convert("RGB")
    return image_with_annotation_box
