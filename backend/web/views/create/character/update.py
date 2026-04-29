import os

from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from web.models.knowledge import Knowledge
from web.models.character import Character
from web.views.utils.photo import remove_old_photo


class UpdateCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            character_id = request.data['character_id']
            character = Character.objects.get(id=character_id, author__user=request.user)
            model = request.data['model'].strip()
            name = request.data['name'].strip()
            profile = request.data['profile'].strip()[:100000]
            photo = request.FILES.get('photo', None)
            background_image = request.FILES.get('background_image', None)

            knowledgeFile = request.FILES.get('knowledgeFile', None)
            print(knowledgeFile)

            fileName, ext = os.path.splitext(knowledgeFile.name)

            if not name:
                return Response({
                    'result': "名字不能为空"
                })
            if not profile:
                return Response({
                    'result': '角色介绍不能为空'
                })
            if photo:
                remove_old_photo(character.photo)
                character.photo = photo
            if background_image:
                remove_old_photo(character.background_image)
                character.background_image = background_image
            character.name = name
            character.profile = profile

            character.model = model

            character.update_time = now()
            character.save()

            knowledge = Knowledge.objects.create(
                character=character,
                fileName=fileName,
                fileType=ext,
            )

            from web.documents.utils import insert_documents
            insert_documents.insert_documents(knowledgeFile,knowledge.id,character.id)

            return Response({
                'result': 'success',
            })
        except Exception as e:
              import traceback
              traceback.print_exc()
              return Response({
                  'result':'系统异常'
              })
