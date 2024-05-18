import uuid

import werkzeug
from flask_restx import Namespace, Resource, reqparse

from handler import StorageHandler

storage_handler = StorageHandler()

files_namespace = Namespace('files', description='File Management')

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')


@files_namespace.route('/upload', methods=["POST"])
class UploadFile(Resource):
    @files_namespace.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()

        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())

        # Global dictionary to store file metadata
        file_metadata = {}

        # Store the file and its metadata
        file_metadata[file_id] = {
            'filename': args['file'].filename,
            'content_type': args['file'].mimetype,
            'size': args['file'].content_length
        }

        # Check if file_metadata contains the required keys
        if 'filename' not in file_metadata[file_id] or 'content_type' not in file_metadata[file_id] or 'size' not in \
                file_metadata[file_id]:
            return {"error": "Failed to extract file metadata"}, 500

        print(file_metadata[file_id])
        # Save the file content to the database
        storage_handler.add_file(
            file_id,
            file_metadata[file_id]['filename'],
            file_metadata[file_id]['content_type'],
            file_metadata[file_id]['size'],
            args['file'].read()
        )

        return {'message': 'File uploaded successfully', 'id': file_id}


@files_namespace.route('/files', methods=["GET"])
class GetAllFiles(Resource):
    def get(self):
        result = storage_handler.get_all()

        return result


getid_parser = reqparse.RequestParser()
getid_parser.add_argument('id', type=str, help="Unique ID generated for that file",
                          trim=True, required=True, nullable=False)


@files_namespace.route('/file/id', methods=["GET"])
class GetIdFile(Resource):
    @files_namespace.expect(getid_parser)
    def get(self):
        args = upload_parser.parse_args()
        content_id = args.get('id')
        result = storage_handler.get_by_id(content_id)
        return result


rename_parser = reqparse.RequestParser()
rename_parser.add_argument('id', type=str, help="Unique ID generated for that file",
                           trim=True, required=True, nullable=False)
rename_parser.add_argument('new_name', type=str, help="New Name for file",
                           trim=True, required=True, nullable=False)


@files_namespace.route('/update/id', methods=["PUT"])
class UpdateIdFile(Resource):
    @files_namespace.expect(rename_parser)
    def get(self):
        args = upload_parser.parse_args()
        content_id = args.get('id')
        new_name = args.get('new_name')
        result = storage_handler.update_by_id(content_id, new_name)
        return None


deleteid_parser = reqparse.RequestParser()
deleteid_parser.add_argument('id', type=str, help="Unique ID generated for that file",
                             trim=True, required=True, nullable=False)


@files_namespace.route('/file/id', methods=["GET"])
class GetIdFile(Resource):
    @files_namespace.expect(deleteid_parser)
    def get(self):
        args = upload_parser.parse_args()
        content_id = args.get('id')
        result = storage_handler.delete_by_id(content_id)
        return None
