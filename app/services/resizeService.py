from celery import Celery
from PIL import Image
import logging
import base64
import os
import moviepy.editor as mp
from .. import settings
from ..models.fileType import fileType
from ..dm_model.story import Story
from ..dm_model import db
# from flask import current_app

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

# Task to resize the image
@celery.task(bind=True)
def async_resize(self, story_id, type ,file_path):
    print('called', type)

    if type == fileType.IMAGE:
        resize_image(file_path)
    else:
        resize_video(file_path)

    update_resize_status(story_id, True)

def resize_video(file_path):

    logger.info("Started resizing...")
    # update_state(state='IN_PROGRESS', meta=None)

    clip = mp.VideoFileClip(file_path)
    logger.info('Got clip from path', file_path)
    clip_resized = clip.resize(height=settings.VIDEO_QUALITY)
    logger.info('Resized will start writing')
    clip_resized.write_videofile(file_path)

    # Sleep to test task status
    logger.info("Completed resizing...")
    # Remove the temporary file


def resize_image(file_path):
    logger.info("Started resizing...")
    # update_state(state='IN_PROGRESS', meta=None)

    img = Image.open(file_path)

    rgb_img = img.convert('RGB')
    width, height  = rgb_img.size
    if width > settings.MAX_WIDTH:
        width = settings.MAX_WIDTH
    if height > settings.MAX_HEIGHT:
        height = settings.MAX_HEIGHT

    new_img = rgb_img.resize((width,height), Image.ANTIALIAS)
    new_img.save(file_path,'JPEG',optimize=True, quality=100)

    # Sleep to test task status
    logger.info("Completed resizing...")
    # Remove the temporary file

def check_status(task_id):
    task = celery.AsyncResult(task_id)
    state = {'status': task.status, 'info': task.info}
    return state


def update_resize_status(story_id, success):
    print('i am updating success')
    print(story_id)
    story = Story.query.filter_by(id=story_id).first()
    print(story)
    if story != None:
        story.resized = success
        db.session.commit()

