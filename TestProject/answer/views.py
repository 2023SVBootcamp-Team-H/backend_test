from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Answer
from worry.models import Worry

# 모든 답변 조회


@api_view(['GET'])
def get_all_answer(request):
    answers = Answer.objects.all()
    content = []
    for answer in answers:
        content.append({
            "question": answer.worry.content,
            "content": answer.content
        })
    return Response(content)

# 특정 id 답변 조회


@api_view(['GET'])
def get_one_answer(request):
    id = request.GET.get("answer_id")
    try:
        answer = Answer.objects.get(id=id)
        content = f"{id}번째 답변 : {answer.content}"
        return Response(content)
    except Answer.DoesNotExist:
        return Response(status=404, data=f"{id}번째 답변이 없습니다.")

# 답변 생성


@api_view(['POST'])
def post_answer(request):
    content = request.data['content']
    question_id = request.data['question_id']
    try:
        question = Worry.objects.get(id=question_id)
        answer = Answer.objects.create(content=content, worry=question)
        return Response(status=201, data=f"{answer.id}번째 답변이 생성되었습니다.")
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{question_id}번째 고민이 없습니다.")

# 답변 수정


@api_view(['PUT'])
def update_answer(request):
    id = request.data['id']
    content = request.data['content']
    try:
        answer = Answer.objects.get(id=id)
        answer.content = content
        answer.save()
        return Response(status=200, data=f"{id}번째 답변이 수정되었습니다.")
    except Answer.DoesNotExist:
        return Response(status=404, data=f"{id}번째 답변이 없습니다.")

# 답변 삭제


@api_view(['DELETE'])
def delete_answer(request):
    id = request.data['id']
    try:
        answer = Answer.objects.get(id=id)
        answer.delete()
        return Response(status=200, data=f"{id}번째 답변이 삭제되었습니다.")
    except Answer.DoesNotExist:
        return Response(status=404, data=f"{id}번째 답변이 없습니다.")
