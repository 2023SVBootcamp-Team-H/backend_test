from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import dotenv
import os

from .models import Worry
from user.models import User
from category.models import Category
from personality.models import Personality
from answer.models import Answer
dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def gpt_answer(json_data):
    import openai  # for OpenAI API calls
    openai.api_key = SECRET_KEY
    if json_data["sex"] == "male" or json_data["sex"]=="Male":
        sex = "남자"
    else:
        sex = "여자"
    
    age = json_data["age"]
    job = json_data["job"]
    address = json_data["address"]
    name = json_data["nickname"]
    
    content = json_data["content"]
    
    category = json_data["category"]
    personality = json_data["personality"]
    
    worry = json_data["worry"]
    
    # send a ChatCompletion request to count to 100
    messages = [
        {'role': 'system', 'content': '안녕하세요. 저는 당신의 고민을 들어주는 챗봇입니다.'},
        {'role':'user',"content":f"안녕하세요. 저는 {address}에 살고, {job}일을 하는 {age}살 {sex} {name}입니다."},
        {'role': 'user', 'content': f"{category}에 대한 고민이 있습니다.어떤 고민이냐면요,"},
        {'role': 'user', 'content': f"{content}"},
        {'role': 'user', 'content': f"{personality}처럼 말해주세요."},
    ]
    
    
    # send a ChatCompletion request to GPT-3.5-turbo model
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.6,  # 조정 가능한 매개변수. 낮을수록 보수적, 높을수록 다양한 응답
        stream = False, # 추후에 True로 변경 예정
        max_tokens=50,  # 생성된 응답의 최대 토큰 수
        n=1,  # 생성할 응답의 수
        stop=None,  # 생성 중지 토큰 (optional)
        log_level="info"  # 응답 로깅 레벨 (optional)
    )
    for chunk in response:
        print(chunk['choices'][0]['delta']["content"],end="",flush=True)
    ans = Answer(worry = worry, content ="")
    return response

worry_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "sex": openapi.Schema(type=openapi.TYPE_STRING),
        "age": openapi.Schema(type=openapi.TYPE_INTEGER),
        "job": openapi.Schema(type=openapi.TYPE_STRING),
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
def get_all_worry(request):
    worries = Worry.objects.all()
    content = []
    for worry in worries:
        content.append({
            'id': worry.id,
            'content': worry.content
        })
    return Response(content)

# 특정 id 고민 조회

@api_view(['GET'])
def get_one_worry(request):
    id = request.GET.get("worry_id")
    try:
        worry = Worry.objects.get(id=id)
        content = f"{id}번째 고민 : {worry.content}"
        return Response(content)
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")

# 고민 생성

@swagger_auto_schema(
    method='post',
    request_body=worry_request_body_schema,
    operation_description="고민 생성",
    )
@api_view(['POST'])
def post_worry(request:Request):
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
    
    # category info
    category = request.data['category']
    
    # personality info
    personality = request.data['personality']
    
    # user register
    user_info = User(sex=sex,age=age,job=job,nickname=nickname,address=address)
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
    
    worry = Worry.objects.create(user=user_info,category=category_info,personality=personality_info,content=content)
    
    json_data = {
        "name":nickname,
        "sex":sex,
        "age":age,
        "job":job,
        "address":address,
        "content":content,
        "category":category,
        "personality":personality,
        "worry":worry,
    }
    return gpt_answer(json_data)



# 고민 수정


@api_view(['PUT'])
def update_worry(request:Request):
    id = request.data['id']
    content = request.data['content']
    try:
        worry = Worry.objects.get(id=id)
        worry.content = content
        worry.save()
        return Response(status=200, data=f"{id}번째 고민이 수정되었습니다.")
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")


# 고민 삭제


@api_view(['DELETE'])
def delete_worry(request:Request):
    id = request.data['id']
    try:
        worry = Worry.objects.get(id=id)
        worry.delete()
        return Response(status=200, data=f"{id}번째 고민이 삭제되었습니다.")
    except Worry.DoesNotExist:
        return Response(status=404, data=f"{id}번째 고민이 없습니다.")
