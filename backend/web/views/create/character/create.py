import os

from langchain_text_splitters import character
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.knowledge import Knowledge
from web.models.character import Character
from web.models.user import UserProfile
from web.documents.utils import insert_documents

class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user

            knowledgeFile = request.FILES.get('knowledgeFile', None)

            fileName, ext = os.path.splitext(knowledgeFile.name)


            user_profile = UserProfile.objects.get(user=user)
            name = request.data.get('name').strip()
            profile = request.data.get('profile').strip()[:100000]
            photo = request.FILES.get('photo', None)
            background_image = request.FILES.get('background_image', None)

            model = request.data.get('model').strip()


            if not name:
                return Response({
                    'result': '名字不能为空'
                })
            if not profile:
                return Response({
                    'result': '角色介绍不能为空'
                })
            if not photo:
                return Response({
                    'result': '头像不能为空'
                })
            if not background_image:
                return Response({
                    'result': '聊天背景不能为空'
                })

            character = Character.objects.create(
                author=user_profile,
                name=name,
                profile=profile,
                photo=photo,
                background_image=background_image,
                model=model,
            )
            print(character)


            knowledge = Knowledge.objects.create(
                character=character,
                fileName=fileName,
                fileType=ext,
            )

            insert_documents.insert_documents(knowledgeFile,knowledge.id,character.id)

            return Response({
                'result': 'success',
            })
        except Exception as e:
            import traceback
            traceback.print_exc()  # 在终端打印完整错误
            return Response({
           'result': f'系统异常：{str(e)}'
             })
