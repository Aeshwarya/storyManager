from celery import Celery
from PIL import Image
import logging
import base64
import os
import moviepy.editor as mp
from .. import settings
from ..models.fileType import fileType

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

# Task to resize the image
@celery.task(bind=True)
def async_resize(self, type ,file_uuid, file):

    if type == fileType.IMAGE:
        self.resize_image(file_uuid, file)
    else:
        self.resize_vedio(file_uuid , file)

def resize_vedio(self, file, file_uuid):

    logger.info("Started resizing...")
    self.update_state(state='IN_PROGRESS', meta=None)

    temp_filename = file_uuid + "_temp.mp4"
    save_path = settings.FILE_STORE_PATH
    with open(save_path+temp_filename, "wb") as fh:
        fh.write(file)

    new_filename = file_uuid + ".mp4"
    clip = mp.VideoFileClip(save_path+temp_filename)
    clip_resized = clip.resize(settings.VEDIO_QUALITY)
    clip_resized.write_videofile(new_filename)
    with open(save_path, "wb") as fh:
        fh.write(clip_resized)

    # Sleep to test task status
    logger.info("Completed resizing...")
    # Remove the temporary file
    try:
        os.remove(save_path+temp_filename)
    except OSError:
        pass
    return save_path+new_filename



def resize_image(self ,file_uuid  , img_string):
    logger.info("Started resizing...")
    self.update_state(state='IN_PROGRESS', meta=None)

    temp_filename = file_uuid + "_temp.jpg"
    save_path = settings.FILE_STORE_PATH
    with open(save_path+temp_filename, "wb") as fh:
        fh.write(img_string)
    img = Image.open(temp_filename)

    rgb_img = img.convert('RGB')
    new_filename = file_uuid + ".jpg"
    width, height  = rgb_img.size
    if width > settings.MAX_WIDTH:
        width = settings.MAX_WIDTH
    if height > settings.MAX_HEIGHT:
        height = settings.MAX_HEIGHT

    new_img = rgb_img.resize((width,height), Image.ANTIALIAS)
    new_img.save(new_filename,'JPEG',optimize=True, quality=100)
    with open(save_path, "wb") as fh:
        fh.write(new_img)
    # Sleep to test task status
    logger.info("Completed resizing...")
    # Remove the temporary file
    try:
        os.remove(save_path+temp_filename)
    except OSError:
        pass
    return save_path+new_filename


def check_status(task_id):
    task = celery.AsyncResult(task_id)
    state = {'status': task.status, 'info': task.info}
    return state
