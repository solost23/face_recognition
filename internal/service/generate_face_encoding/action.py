import io
import json
import re

import face_recognition as fr

from internal.service.base import action

from protopb.gen.py3.protos.face_recognition import face_recognition_pb2 as face_recognition


class Action(action.Action):
    def __init__(self, context):
        self.context = context

    def deal(self, request, context):
        """login"""
        return deal(self, request, context)


def deal(self, request, context):
    # 校验参数
    if len(request.data) <= 0:
        return face_recognition.GenerateFaceEncodingResponse(faceEncodings=[])

    files = []
    for data in request.data:
        files.append(io.BytesIO(data))

    face_imgs = []
    for file in files:
        face_imgs.append(fr.load_image_file(file))

    face_encodings = []
    for face_img in face_imgs:
        face_encoding = fr.face_encodings(face_img)
        if len(face_encoding) < 0:
            context.set_detail("图片未发现人脸，请重新获取图片")
        if len(face_encoding) > 1:
            context.set_detail("不支持多张人脸进行注册")

        face_encodings.append(json.dumps(face_encoding[0].tolist()))

    return face_recognition.GenerateFaceEncodingResponse(faceEncodings=face_encodings)

