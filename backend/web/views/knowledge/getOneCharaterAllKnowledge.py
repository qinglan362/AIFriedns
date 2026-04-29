from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models import Knowledge



class GetOneCharacterAllKnowledge(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            id = request.query_params.get('character_id')
            print(id)
            knowledge_raw = Knowledge.objects.filter(
                character__id=request.query_params.get('character_id')
            ).order_by('-create_time')
            print(knowledge_raw)
            knowledges = []
            for knowledge in knowledge_raw:
                character = knowledge.character
                author = character.author
                knowledges.append({
                    'id': knowledge.id,
                    'character': {
                        'id': character.id,
                        'name': character.name,
                        'profile': character.profile,
                        'photo': character.photo.url,
                        'background_image': character.background_image.url,
                        'model': character.model,
                        'author': {
                            'user_id': author.user_id,
                            'username': author.user.username,
                            'photo': author.photo.url,
                        }
                    },
                    'knowledge': {
                        'fileName': knowledge.fileName,
                        'fileType': knowledge.fileType,
                        'createTime': knowledge.create_time,
                    }
                })
            return Response({
                'result': 'success',
                'knowledges': knowledges,
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })
