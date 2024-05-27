import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(f'Maximum allowed size for the image are 70x70 - size of image you uploaded: {img.size}')
            
def validate_image_file_extensions(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    if not ext.lower() in valid_extensions:
        raise ValidationError(f'That extension is not allowed to be uploaded - Ext: {ext}')