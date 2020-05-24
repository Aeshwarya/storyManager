from ..models.fileType import fileType
from . import  ResizeService
from ..dm_model.story import Story
from ..dm_model import db

class StoryService():

    def createStory(self, data):
        username = data.user_name
        story_name = data.name
        description = data.description
        type_of_story = data.type
        latitude = data.latitude
        longitude = data.longitude
        new_file_uuid = self.add_story(username , story_name , description, type_of_story, latitude, longitude , data)
        if type == fileType.IMAGE:
            file_data = data.image
        elif type == fileType.VEDIO:
            file_data = data.vedio
        else:
            file_data = data.text
        location = ResizeService.async_resize.B(new_file_uuid, file_data)
        self.update_file_location(new_file_uuid, location)


    def add_story(self, username , story_name , desc, type_of_story, lat, long , data):
        with self.app.app_context():
            new_story = Story(user_name=username, story_name=story_name, description=desc, type_of_story=type_of_story, latitude=lat, longitude=long)
            db.session.add(new_story)
            db.session.commit()
            id = new_story.id
        return id

    def update_file_location(self, new_file_uuid , location):
        with self.app.app_context():
            story = Story.query.filter_by(id=new_file_uuid).first()
            story.file_data_location = location
            db.session.commit()

    def fetchStory(self, story_id):



    def fetchResizedContent(self, story_id):


    def fetchAllStory(self):




