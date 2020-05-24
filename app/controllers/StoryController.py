from flask import Flask, make_response, Blueprint, current_app, jsonify, request
from ..services import StoryService
from ..models.story import Story

StoryController = Blueprint('story_controller', __names__)

@StoryController.route("/create/story", methods=['POST'])
def add_story():
    resp = {}
    try:
        print(request)
        data = request.get_json()

        username = data.user_name
        story_name = data.name
        description = data.description
        type_of_story = data.type
        latitude = data.latitude
        longitude = data.longitude

        story_obj = Story(username, story_name, description, type_of_story, latitude, longitude, data)

        if type == fileType.IMAGE:
            file_data = data.image
        elif type == fileType.VEDIO:
            file_data = data.vedio
        else:
            file_data = data.text
        location = ResizeService.async_resize.B(new_file_uuid, file_data)
        self.update_file_location(new_file_uuid, location)





        StoryService.createStory(data)





@StoryController.route("/", methods=['GET'])
def get_story():


@StoryController.route("/", methods=['POST'])
def get_all_Stories():




@StoryController.route("/", methods=['POST'])
def get_resized_photo():

