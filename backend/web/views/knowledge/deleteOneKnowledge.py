from unittest import result

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models import  Knowledge
from web.documents.utils import insert_documents


class DeleteOneKnowledge(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            knowledge_id = int(request.data.get('knowledge_id'))
            Knowledge.objects.filter(id=knowledge_id).delete()
            print("shanchu")
            insert_documents.delete_documents(knowledge_id)
            return Response({
                'result':'success'
            })
        except Exception as e:
             import traceback
             traceback.print_exc()
             return Response({'result': f'系统异常: {str(e)}'})


