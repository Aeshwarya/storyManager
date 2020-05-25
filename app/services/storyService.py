from ..models.fileType import fileType
from . import  resizeService
from ..dm_model.story import Story
from ..dm_model import db
from .baseService import BaseService


class StoryService(BaseService):

    def __init__(self, app):
        BaseService.__init__(self , app)

    def createStory(self, story_obj):
        new_file_uuid = self.add_story(story_obj)
        print("story_obj", story_obj)
        if story_obj.type_of_story != fileType.TEXT:
            resizeService.async_resize.delay(new_file_uuid, story_obj.type_of_story, story_obj.data)

        print(new_file_uuid)
        return new_file_uuid

    def add_story(self, story_obj):
        id = None
        with self.app.app_context():
            new_story = Story(user_name=story_obj.user_name, story_name=story_obj.story_name, description=story_obj.description, type_of_story=story_obj.type_of_story, latitude=story_obj.latitude, longitude=story_obj.longitude, data=story_obj.data)
            db.session.add(new_story)
            db.session.commit()
            id = new_story.id
        return id


    def fetchStory(self, story_id):
        story = None
        with self.app.app_context():
            story = Story.query.filter_by(id = story_id).first()
        return story

    def fetchAllStory(self):
        resp = {}
        with self.app.app_context():
            stories = Story.query.order_by(Story.date_created.desc()).all()
            for s in stories:
                id = s.id
                resp[id] = self.getStory(s)
            return resp

    def getStory(self, s):
        story = {}
        story["user_name"] = s.user_name
        story["story_name"] = s.story_name
        story["description"] = s.description
        story["type_of_story"] = s.type_of_story.value
        if s.type_of_story.value == "TEXT":
            story["data"] = s.data
        story["created_data"] = s.date_created
        story["latitude"] = s.latitude
        story["longitude"] = s.longitude
        return story
