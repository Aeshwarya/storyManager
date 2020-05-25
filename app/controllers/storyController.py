from flask import Flask, make_response, Blueprint, current_app, jsonify, request , send_from_directory
from ..services.storyService import StoryService
from ..models.story import Story
from ..file_store.fileStore import FileStore
from ..models.fileType import fileType
import  os

StoryService = StoryService(current_app)
StoryController = Blueprint('story_controller', __name__)

@StoryController.route("/story", methods=['POST'])
def add_story():
    resp = { }
    try:
        data = request.form.to_dict()

        print(data)

        username = data['user_name']
        story_name = data['name']
        description = data['description']
        type_of_story = data['type']
        latitude = data['latitude']
        longitude = data['longitude']

        file_data = None

        if type_of_story != fileType.TEXT:
            file = request.files['file']
            
            if (file == None or not allowed_file(current_app, file.filename) ):
                resp["error"] = "File not supported"
                resp["status"] = 400
                return make_response(resp, resp["status"]) 

            extension = '.jpeg'

            if type_of_story == fileType.VIDEO:
                extension = '.mp4'
            
            print(extension)
            file_data = FileStore().storeFileAndGetLocation(file, extension)
        else:
            file_data = data['text']

        story_obj = Story(username, story_name, description, type_of_story, file_data, latitude, longitude)
        story_id = StoryService.createStory(story_obj)

        return make_response(str(story_id))
    except Exception as e:
        resp["error"] = "some error occured in creating story"
        resp["status"] = 400
        return make_response(resp, resp["status"]) 


@StoryController.route("/stories", methods=['GET'])
def get_all_Stories():
    resp = {}
    try:
        stories = StoryService.fetchAllStory()
        return make_response(jsonify(stories), 200)
    except Exception as e:
        print(e)
        resp["error"] = "some error occured in fetching stories"
        resp["status"] = 400
    return make_response(resp, resp["status"])



@StoryController.route("/resize", methods=['GET'])
def get_resized_photo():
    resp =  {}
    try:
        story_id = request.args.get("story_id")
        story = StoryService.fetchStory(story_id)
        if story.type_of_story != fileType.TEXT and story.data != None and story.resized == True:
            return send_from_directory(os.path.dirname(story.data), os.path.basename(story.data))
        else:
            resp["error"] = "file not found can be because resize is not complete or story does not have a video or photo attached to it"
            resp["status"] = 404

    except Exception as e:
        print(e)
        resp["error"] = "some error occured in getting resized story"
        resp["status"] = 500

    return make_response(resp, resp["status"])


def allowed_file(app, filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

