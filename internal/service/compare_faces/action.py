import io, numpy, json

from internal.service.base import action
import face_recognition as fr
from protopb.gen.py3.protos.face_recognition import face_recognition_pb2 as face_recognition


class Action(action.Action):
    def __init__(self, context):
        self.context = context

    def deal(self, request, context):
        """login"""
        return deal(self, request, context)


def deal(self, request, context):
    if len(request.data) <= 0:
        return face_recognition.CompareFacesResponse(userId='', isFound=False)

    # 获取人脸信息
    auth_face = fr.face_encodings(fr.load_image_file(io.BytesIO(request.data)))
    if len(auth_face) <= 0:
        return face_recognition.CompareFacesResponse(userId='', isFound=False)
    if len(auth_face) > 1:
        return context.set_details('不支持多张人脸进行认证')

    # 与脸库对比
    known_face_encodings = []
    user_ids = []

    for user in self.get_mongo()['twitta']['users'].find():
        known_face_encodings.append(json.loads(user.get('face_encoding')))
        user_ids.append(user.get('_id'))

    try:
        compare_faces = fr.compare_faces(numpy.array(known_face_encodings), auth_face)
    except Exception as e:
        context.set_details(e)

    if True not in compare_faces:
        return face_recognition.CompareFacesResponse(userId='', isFound=False)

    p = compare_faces.index(True)
    if p == -1:
        return face_recognition.CompareFacesResponse(userId='', isFound=False)
    return face_recognition.CompareFacesResponse(userId=user_ids[p], isFound=True)



