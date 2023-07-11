from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import dotenv
import openai
import os

from .models import Worry
from user.models import User
from category.models import Category
from personality.models import Personality
from answer.models import Answer

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def gpt_answer(json_data):
    # for OpenAI API calls
    openai.api_key = SECRET_KEY
    if json_data["sex"] == "male" or json_data["sex"] == "Male":
        sex = "남자"
    else:
        sex = "여자"

    age = json_data["age"]
    job = json_data["job"]
    address = json_data["address"]
    name = json_data["name"]

    content = json_data["content"]

    category = json_data["category"]
    personality = json_data["personality"]

    worry = json_data["worry"]

    # send a ChatCompletion request to count to 100
    messages = [
        {'role': 'system', 'content': '안녕하세요. 저는 당신의 고민을 들어주는 챗봇입니다.'},
        {'role': 'user', "content": f"안녕하세요. 저는 {address}에 살고, {job}일을 하는 {age}살 {sex} {name}입니다."},
        {'role': 'user', 'content': f"{category}에 대한 고민이 있습니다.어떤 고민이냐면요,"},
        {'role': 'user', 'content': f"{content}"},
        {'role': 'user', 'content': f"{personality}처럼 말해주세요."},
        {'role': 'user', 'content': f"40글자 안으로 대답해줘."}
    ]

    # send a ChatCompletion request to GPT-3.5-turbo model
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.4,  # 조정 가능한 매개변수. 낮을수록 보수적, 높을수록 다양한 응답
        stream=False,  # 추후에 True로 변경 예정
        max_tokens=450,  # 생성할 최대 토큰 수
        n=1,  # 생성할 응답의 수
        stop=None  # 생성 중지 토큰 (optional)
    )
    
    responded_answer = Answer(worry=worry, content=response['choices'][0]["message"]["content"])
    responded_answer.save()
    print(response['choices'][0]["message"]["content"])
    return response['choices'][0]["message"]["content"]


worry_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "sex": openapi.Schema(type=openapi.TYPE_STRING),
        "age": openapi.Schema(type=openapi.TYPE_INTEGER),
        "job": openapi.Schema(type=openapi.TYPE_STRING),
        "nickname": openapi.Schema(type=openapi.TYPE_STRING),
        "address": openapi.Schema(type=openapi.TYPE_STRING),
        'content': openapi.Schema(type=openapi.TYPE_STRING),
        'category': openapi.Schema(type=openapi.TYPE_STRING),
        'personality': openapi.Schema(type=openapi.TYPE_STRING),

    }
)


# query string : /worry/?worry_id=1
# -> request.GET.get("worry_id") == 1

# path parameter : /worry/1/
# -> request["worry_id"] == 1

# 모든 고민 조회
@api_view(['GET'])
def get_one_worry(request, worry_id):
    id = worry_id
    try:
        worry = Worry.objects.get(id=id)
        content = f"{id}번째 고민 : {worry.content}"
        return Response(content)
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")

# 특정 id 고민 조회


@swagger_auto_schema(
    method='get',
    operation_description="고민 전체 조회",
)
@swagger_auto_schema(
    method='post',
    request_body=worry_request_body_schema,
    operation_description="고민 생성",
)
@swagger_auto_schema(
    method='delete',
    operation_description="고민 post.body.id에 해당하는 고민 삭제"
)
@swagger_auto_schema(
    method='put',
    operation_description="post.body.id에 해당하는 고민 덮어쓰기 post.body.content가 필요"
)
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def get_all_worry(request: Request):
    if request.method == 'GET':
        worries = Worry.objects.all()
        content = []
        for worry in worries:
            content.append({
                'id': worry.id,
                'content': worry.content,
            })
        return Response(content)
    elif request.method == 'POST':
        # user info
        sex = request.data["sex"]
        age = request.data["age"]
        job = request.data["job"]
        nickname = request.data["nickname"]
        address = request.data["address"]
        if sex == None or age == None or job == None or address == None or nickname == None:
            return Response(status=404, data=f"잘못된 입력입니다.")
        # worry info
        content = request.data['content']
        if content == None or len(content) == 0:
            return Response(status=404, data=f"잘못된 입력입니다.")

        # category info
        category = request.data['category']
        if Category.objects.filter(name=category).first() is None and len(category) != 0:
            return Response(status=404, data=f"등록된 카테고리가 없습니다.")

        # personality info
        personality = request.data['personality']
        if Personality.objects.filter(name=personality).first() is None and len(personality) != 0:
            return Response(status=404, data=f"등록된 인물이 없습니다.")

        # user register
        user_info = User(sex=sex, age=age, job=job,
                         nickname=nickname, address=address)
        user_info.save()

        try:
            # category load
            category_info = Category.objects.filter(name=category).first()

            # personality frequency + 1
            personality_info = Personality.objects.filter(name=personality).first()
            personality_info.frequency += 1
            personality_info.save()
        except Exception as e:
            return Response(status=404, data=f"{e}")

        worry = Worry.objects.create(
            user=user_info, category=category_info, personality=personality_info, content=content)

        json_data = {
            "name": nickname,
            "sex": sex,
            "age": age,
            "job": job,
            "address": address,
            "content": content,
            "category": category,
            "personality": personality,
            "worry": worry,
        }
        return Response(status=200, data=gpt_answer(json_data))
    elif  request.method == 'PUT':
        id = request.data['id']
        content = request.data['content']
        try:
            worry = Worry.objects.get(id=id)
            worry.content = content
            worry.save()
            return Response(status=200, data=f"{id}번째 고민이 수정되었습니다.")
        except Worry.DoesNotExist:
            return Response(status=404, data=f"{id}번째 고민이 없습니다.")
    elif request.method == 'DELETE':
        id = request.data['id']
        try:
            worry = Worry.objects.get(id=id)
            worry.delete()
            return Response(status=200, data=f"{id}번째 고민이 삭제되었습니다.")
        except Worry.DoesNotExist:
            return Response(status=404, data=f"{id}번째 고민이 없습니다.")


