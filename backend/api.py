from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug, os

from detect import *
from sentense_maker import *
from visionres_parser import *

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "myfirstproject.json"

app = Flask(__name__)
api = Api(app)
UPLOAD_FOLDER = './uploads'
parser = reqparse.RequestParser()
parser.add_argument('pic', type=werkzeug.datastructures.FileStorage, location='files')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class PhotoUpload(Resource):
    decorators=[]

    def post(self):
        data = parser.parse_args()
        if data['pic'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        photo = data['pic']

        if photo:
            filename = 'your_image.png'
            photo.save(os.path.join(UPLOAD_FOLDER,filename))
            #data = "test sentense"
            data = detect('uploads/your_image.png')
            data = make_sentense_from_raw(data)
            
            return {
                    'data':data,
                    'status':'success'
                    }
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }


api.add_resource(HelloWorld, '/')
api.add_resource(PhotoUpload,'/upload')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)