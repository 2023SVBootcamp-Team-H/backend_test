import json
import time

from django.core.handlers.wsgi import WSGIRequest
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.forms.models import model_to_dict
from drf_yasg import openapi
import dotenv
import openai
import os

from .models import Worry
from user.models import User
from category.models import Category
from personality.models import *
from answer.models import Answer

dotenv.load_dotenv("/config/.env")
SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")


def gpt_answer(json_data, p: Personality):
    # for OpenAI API calls
    openai.api_key = SECRET_KEY
    if json_data["gender"] == "male" or json_data["gender"] == "Male":
        gender = "남자"
    else:
        gender = "여자"

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
        {'role': 'user', 'content': f"30글자 안으로 {personality}처럼 대답해."},
        {'role': 'user', "content": f"안녕.{address}에 살고, {job}일을 하는 {age}살 {gender} {name}이야."},
    ]
    messages.extend(best_worry_answer(p, 5))
    messages.extend([
        {'role': 'user', 'content': f"{category}에 대한 고민"},
        {'role': 'user', 'content': f"{content}"},
        {'role': 'user', 'content': f"어떻게 해야할까?"}
    ])

    # 추후에 몇개를 페이징 할지 정한다.
    print(messages)
    # send a ChatCompletion request to GPT-3.5-turbo model
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.4,  # 조정 가능한 매개변수. 낮을수록 보수적, 높을수록 다양한 응답
        stream=False,  # 추후에 True로 변경 예정
        # max_tokens=200,  # 생성할 최대 토큰 수
        n=1,  # 생성할 응답의 수
        # 생성 중지 토큰 (optional)
    )

    responded_answer = Answer(worry=worry, content=response['choices'][0]["message"]["content"])
    responded_answer.save()
    print(response['choices'][0]["message"]["content"])
    return {
        "answer_id": responded_answer.pk,
        "message": response['choices'][0]["message"]["content"]
    }

    # return response['choices'][0]["message"]["content"]


worry_request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "gender": openapi.Schema(type=openapi.TYPE_STRING),
        "age": openapi.Schema(type=openapi.TYPE_INTEGER),
        "job": openapi.Schema(type=openapi.TYPE_STRING),
        "nickname": openapi.Schema(type=openapi.TYPE_STRING),
        "address": openapi.Schema(type=openapi.TYPE_STRING),
        'content': openapi.Schema(type=openapi.TYPE_STRING),
        'category': openapi.Schema(type=openapi.TYPE_STRING),
        'personality': openapi.Schema(type=openapi.TYPE_STRING),

    }
)
worry_responses_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'answer_id':openapi.Schema(type=openapi.TYPE_INTEGER),
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        
    },
)
all_worry_responses_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'worry_id':openapi.Schema(type=openapi.TYPE_INTEGER),
        'user': openapi.Schema(type=openapi.TYPE_INTEGER),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER),
        'personality': openapi.Schema(type=openapi.TYPE_INTEGER),
        'content': openapi.Schema(type=openapi.TYPE_STRING),
        'answer': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                 properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "worry_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "content": openapi.Schema(type=openapi.TYPE_STRING),
                "likes": openapi.Schema(type=openapi.TYPE_INTEGER),
            }
            )
           
        )
    }    
)
    
    
worry_responses_schema_404 = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="404 Error입니다."
)


worry_delete_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "worry_id": openapi.Schema(type=openapi.TYPE_INTEGER),
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


@api_view(['GET'])
def get_best_worry_answer(request, page):
    result = []
    for p in Personality.objects.all():
        result.append({
            "personality": model_to_dict(p),
            f"best_worry_answer_page={page}": best_worry_answer(p, page)
        })

    return Response(result)


# 특정 id 고민 조회


@swagger_auto_schema(
    method='get',
    operation_description="고민 전체 조회",
    responses={
        200: all_worry_responses_schema,
    }

)
@swagger_auto_schema(
    method='post',
    request_body=worry_request_body_schema,
    responses={
        200: worry_responses_schema,
        404: worry_responses_schema_404
    },
    operation_description="고민 생성",
)
@swagger_auto_schema(
    method='delete',
    request_body=worry_delete_body_schema,
    operation_description="고민 post.body.worry_id에 해당하는 고민 삭제"
)
@swagger_auto_schema(
    method='put',
    operation_description="post.body.id에 해당하는 고민 덮어쓰기 post.body.content가 필요"
)
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def get_all_worry(request: Request):
    print(request.method)
    if request.method == 'GET':
        result = []
        worries = Worry.objects.all()
        for w in worries:
            w_dict = model_to_dict(w)
            w_dict["answer"] = model_to_dict(w.answer)
            result.append(w_dict)
        return Response(result)

    elif request.method == 'POST':
        # user info
        gender = request.data["gender"]
        age = request.data["age"]
        job = request.data["job"]
        nickname = request.data["nickname"]
        address = request.data["address"]
        if gender == None or age == None or job == None or address == None or nickname == None:
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
        p = Personality.objects.filter(name=personality).first()
        if p is None and len(personality) != 0:
            return Response(status=404, data=f"등록된 인물이 없습니다.")

        # user register
        user_info = User(gender=gender, age=age, job=job,
                         nickname=nickname, address=address)
        user_info.save()

        try:
            # category load
            category_info = Category.objects.filter(name=category).first()

            # personality frequency + 1
            personality_info = p

        except Exception as e:
            return Response(status=404, data=f"{e}")

        worry = Worry.objects.create(
            user=user_info, category=category_info, personality=personality_info, content=content)

        json_data = {
            "name": nickname,
            "gender": gender,
            "age": age,
            "job": job,
            "address": address,
            "content": content,
            "category": category,
            "personality": personality,
            "worry": worry,
        }
        return Response(status=200, data=gpt_answer(json_data, p))
    
    elif request.method == 'PUT':
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
        worry_id = request.data['worry_id']
        print(worry_id)
        try:
            worry = Worry.objects.get(pk=worry_id)
            worry.delete()
            return Response(status=200, data=f"{worry_id}번째 고민이 삭제되었습니다.")
        except Worry.DoesNotExist:
            return Response(status=404, data=f"{worry_id}번째 고민이 없습니다.")


@csrf_exempt
def sse_request(request: WSGIRequest):
    
    # SSE 방식으로 오류 메시지를 반환
    def error_return(error_message: str):
        def error_stream():
            yield f'error_message'
            time.sleep(0.02)
            yield f'{error_message}'


        return StreamingHttpResponse(
            error_stream(), content_type='text/event-stream')

    # request.body = worry_info
    # worry = 성별, 나이, 직업, 닉네임, 주소, 고민내용, 카테고리, 인물
    body = json.loads(request.body)

    print(body)

    gender = body["gender"]
    age = body["age"]
    job = body["job"]
    nickname = body["nickname"]
    address = body["address"]
    content = body['content']
    category = body['category']
    personality = body['personality']

    # gender info
    if gender == None or age == None or job == None or address == None or nickname == None:
        return error_return("잘못된 입력입니다.")
    
    # worry info
    if content == None:
        return error_return("잘못된 입력입니다.")
    
    # category info
    c = Category.objects.filter(name=category).first()
    if c is None:
        return error_return("등록된 카테고리가 없습니다.")
    
    # personality info
    p = Personality.objects.filter(name=personality).first()
    if p is None:
        return error_return("등록된 인물이 없습니다.")

    
    
    # user register
    user_info = User.objects.create(gender=gender, age=age, job=job, nickname=nickname, address=address)

    # worry register
    worry = Worry.objects.create(user=user_info, category=c, personality=p, content=content)

    def event_stream():

        openai.api_key = SECRET_KEY

        messages = []
        
        # p.content : dump된 json
        # 고정된 답변
        messages.extend(json.loads(p.content))
        
        # 평점이 좋았던 답변들 5개 등록
        messages.extend(best_worry_answer(p, 5))
        
        # 고민 넣기
       #messages.append({'role': 'user', 'content': f"\"{body['content']}\"{p.static_personality.prompt}"})
        prompt = p.static_personality.prompt.replace("{content}", content)
        messages.append({'role': 'user', 'content': prompt})
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=p.static_personality.temperature,
            max_tokens=p.static_personality.max_tokens,
            top_p=p.static_personality.top_p,
            frequency_penalty=p.static_personality.frequency_penalty,
            presence_penalty=p.static_personality.presence_penalty,
            stop=p.static_personality.stop,
            stream=True,  # 추후에 True로 변경 예정
        )
        answer = ""

        # stream의 갯수만큼 보낸다.
        for r in res:
            rs = r["choices"][0]

            if rs["finish_reason"] == "stop":
                break
            else:
                yield '{}'.format(rs["delta"]["content"])
                answer += rs["delta"]["content"]

        register_answer = Answer(worry=worry, content=answer)
        register_answer.save()

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'  # 캐시를 사용하지 않음
    return response


def best_worry_answer(p: Personality, page: int):
    """
    고민과 답변의 최고 인기있는 리스트를 page수만큼 chatgpt에 넣을수 있게 반환함

    Args:
        p: 인격 객체
        page: 페이징할 int, 답변이 2개인데 3개를 페이징 할경우 2개를 반환한다.

    Returns:
        page수에 맞는 고민, 답 내용을 반환함
[
    {
        "role": "user",
        "content": "고민내용"
    },

    {
        "role": "assistant",
        "content": "답변내용"
    }, ...
]
    """
    result = []
    # 고민중 인격에 맞는 것들중 답변의 좋아요로 내림차순중 최고 좋은 평가를 받은 page만큼 조회
    worries = Worry.objects.filter(personality=p).order_by('-answer__likes')[:page]
    for w in worries:
        # 만약 답변투표를 하지 않은 고민(방금 생성된 고민)이면 pass 한다.
        try:
            w.answer
        except Exception as e:
            continue
        if w.answer.likes is None:
            continue
        result.append({
            "role": "user",
            "content": w.content
        })
        result.append({
            "role": "assistant",
            "content": w.answer.content
        })
    return result
