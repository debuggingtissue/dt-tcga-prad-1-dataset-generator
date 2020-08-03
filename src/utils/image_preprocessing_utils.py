from PIL import Image


def crop_to_the_centermost(image, new_size):
    width, height = image.size  # Get dimensions

    left = (width - new_size) / 2
    top = (height - new_size) / 2
    right = (width + new_size) / 2
    bottom = (height + new_size) / 2

    # Crop the center of the image
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image


def scale_image(image, new_size):
    maxsize = (new_size, new_size)
    image.thumbnail(maxsize, Image.ANTIALIAS)
    return image
