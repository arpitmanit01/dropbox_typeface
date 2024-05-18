# Importing necessary modules
import uuid

import werkzeug
from flask_restx import Namespace, Resource, reqparse

from handler import StorageHandler

# Initialize the storage handler
storage_handler = StorageHandler()

# Define the namespace for file management operations
files_namespace = Namespace('files', description='File Management')

# Parser setup for uploading files
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')


# Route for uploading files
@files_namespace.route('/upload', methods=["POST"])
class UploadFile(Resource):
    @files_namespace.expect(upload_parser)
    def post(self):
        result_msg = None
        try:
            # Parse arguments from the request
            args = upload_parser.parse_args()

            # Generate a unique ID for the file using UUID
            file_id = str(uuid.uuid4())

            # Initialize a dictionary to hold file metadata
            file_metadata = {}

            # Store file metadata including filename, content type, and size
            file_metadata[file_id] = {
                'filename': args['file'].filename,
                'content_type': args['file'].mimetype,
                'size': args['file'].content_length
            }

            # Validate file metadata
            if 'filename' not in file_metadata[file_id] or 'content_type' not in file_metadata[file_id] or 'size' not in \
                    file_metadata[file_id]:
                return {"error": "Failed to extract file metadata"}, 500

            # Print file metadata for debugging purposes
            print(file_metadata[file_id])

            # Save the file content to the database using the storage handler
            storage_handler.add_file(
                file_id,
                file_metadata[file_id]['filename'],
                file_metadata[file_id]['content_type'],
                file_metadata[file_id]['size'],
                args['file'].read()
            )
            return {'message': 'File uploaded successfully', 'id': file_id}, 200
        except Exception as e:
            result_msg = {
                'message': str(e)
            }
            return result_msg


# Route for retrieving all files
@files_namespace.route('/files', methods=["GET"])
class GetAllFiles(Resource):
    def get(self):
        try:
            # Retrieve all files from the storage handler
            result = storage_handler.get_all()
            return result, 200
        except Exception as e:
            result_msg = {
                'message': str(e)
            }
            return result_msg


# Parser setup for getting a file by its ID
getid_parser = reqparse.RequestParser()
getid_parser.add_argument('id', type=str, help="Unique ID generated for that file", trim=True, required=True,
                          nullable=False)


# Route for getting a file by its ID
@files_namespace.route('/file/id', methods=["GET"])
class GetIdFile(Resource):
    @files_namespace.expect(getid_parser)
    def get(self):
        try:
            # Parse the ID argument from the request
            args = upload_parser.parse_args()
            content_id = args.get('id')

            # Retrieve the file details by ID using the storage handler
            result = storage_handler.get_by_id(content_id)
            return result
        except Exception as e:
            result_msg = {
                'message': str(e)
            }
            return result_msg


# Parser setup for updating a file name by its ID
rename_parser = reqparse.RequestParser()
rename_parser.add_argument('id', type=str, help="Unique ID generated for that file", trim=True, required=True,
                           nullable=False)
rename_parser.add_argument('new_name', type=str, help="New Name for file", trim=True, required=True, nullable=False)


# Route for updating a file name by its ID
@files_namespace.route('/update/id', methods=["PUT"])
class UpdateIdFile(Resource):
    @files_namespace.expect(rename_parser)
    def put(self):
        try:
            # Parse the ID and new name arguments from the request
            args = upload_parser.parse_args()
            content_id = args.get('id')
            new_name = args.get('new_name')

            # Update the file name in the database using the storage handler
            result = storage_handler.update_by_id(content_id, new_name)
            result_msg = {
                'message': "Update Success"
            }, 200
        except Exception as e:
            result_msg = {
                'message': str(e)
            }
            return result_msg


# Parser setup for deleting a file by its ID
deleteid_parser = reqparse.RequestParser()
deleteid_parser.add_argument('id', type=str, help="Unique ID generated for that file", trim=True, required=True,
                             nullable=False)


# Route for deleting a file by its ID
@files_namespace.route('/file/id', methods=["delete"])
class DeleteIdFile(Resource):
    @files_namespace.expect(deleteid_parser)
    def delete(self):
        try:
            # Parse the ID argument from the request
            args = upload_parser.parse_args()
            content_id = args.get('id')

            # Delete the file from the database using the storage handler
            result = storage_handler.delete_by_id(content_id)
            result_msg = {
                'message': "Delete Success"
            }, 200
        except Exception as e:
            result_msg = {
                'message': str(e)
            }
            return result_msg
