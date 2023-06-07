from protopb.gen.py3.protos.face_recognition import face_recognition_pb2_grpc as face_recognition_grpc

from internal.service.generate_face_encoding import action as generate_face_encoding_action
from internal.service.compare_faces import action as compare_faces_action


class FaceRecognitionService(face_recognition_grpc.faceRecognitionServicer):
   def __init__(self, mongo):
       self.mongo = mongo

   def GenerateFaceEncoding(self, request, context):
      return GenerateFaceEncoding(self, request, context)
   
   def CompareFaces(self, request, context):
      return CompareFaces(self, request, context)


def GenerateFaceEncoding(self, request, context):
    a = generate_face_encoding_action.Action(context)
    a.set_mongo(self.mongo)
    return a.deal(request, context)


def CompareFaces(self, request, context):
   a = compare_faces_action.Action(context)
   a.set_mongo(self.mongo)
   return a.deal(request, context)
        