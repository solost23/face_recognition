from protopb.gen.py3.protos.face_recognition import face_recognition_pb2_grpc as face_recognition_grpc
from internal.service import service


def init(config):
    """
    注册服务
    :return:
    """
    face_recognition_grpc.add_faceRecognitionServicer_to_server(service.FaceRecognitionService(config.mongo), config.server)