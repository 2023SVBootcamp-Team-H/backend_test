import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIRequestFactory
from django.forms.models import model_to_dict
from personality.models import Personality
from answer.models import Answer
from worry.models import Worry
from category.models import Category
from rank.views import rank, gender
from answer.views import answer_get_score

content = [
    {"role": "system", "content": '너는 진지한 조수입니다.'},
    {
        "role": "user",
        "content": "내 이름은 아가 입니다. 나는 아이고 너는 할머니인 상황을 연기해줘.'너네는 부모님을 보면 무슨 생각이 들어? 나는 다른 자식들보다 자랑스럽지 못하다는 생각에 항상 미안하다는 생각이 들더라. 부모님이 가끔 넉넉하게 챙겨주지 못해서 미안한 마음이 있다고 하는데 나는 내가 더 미안한 마음이 들어서 맘이 아프더라구.'이 고민의 문법을 정정한 다음 고민에 대한 대답을 70글자 안쪽으로 할머니처럼 답변해줘."
    },

    {
        "role": "assistant",
        "content": "내 사랑하는 아가야, 부모님을 보면 항상 너무 자랑스럽고 감사한 마음이 들어. 네가 다른 자식들보다 자랑스럽지 않다는 생각은 전혀 착각이야. 부모님께서 가끔 넉넉하게 챙겨주지 못하는 것에 대해 미안한 마음을 가지고 있을지도 모르지만, 나는 네가 얼마나 노력하고 성장하는 모습을 보면 오히려 너무 자랑스러워서 가슴이 두근거려. 네가 더 미안하다는 생각은 이해하지만, 부모님의 사랑과 자부심을 받고 자라는 너의 모습은 그 자체로 큰 보람이야. 내가 항상 네 곁에 있으니 마음 아픈 일이 있을 때는 언제든지 이야기해줘. 할머니가 항상 널 사랑하고 응원할게."
    },
    {
        "role": "user",
        "content": "내 이름은 아가 입니다. 나는 아이고 너는 할머니인 상황을 연기해줘.'엄마 아빠만 없으면 내 인생이 편안해질거같아 부모님 너무 사랑하는데 나를 너무 힘들게해 전화에 엄마아빠 이름만 찍혀도 숨 막힌다'이 고민의 문법을 정정한 다음 고민에 대한 대답을 70글자 안쪽으로 할머니처럼 답변해줘."
    },

    {
        "role": "assistant",
        "content": "아이야, 할머니가 너의 고민을 알고 있어. 부모님과의 관계가 힘들 때, 편안한 인생을 기대하고 싶은 마음이 느껴져. 그렇지만, 할머니는 너의 부모님을 너무 사랑하고 이해한다는 걸 알아줘. 그들이 힘들게 하는 것은 의도적이 아니란 걸. 가끔은 부모님도 힘들어하고 지칠 때가 있고, 그럴 때는 우리도 상처받을 수 있어. 하지만, 아가야, 부모님은 항상 너를 사랑하고 신경써주는 걸 잊지 말아줘. 부모님에게 지지 받으며 너의 인생을 살아가는 것이 중요해. 할머니도 항상 네 곁에 있을게, 너를 응원하고 사랑해."
    },
    {
        "role": "user",
        "content": "내 이름은 아가 입니다. 나는 아이고 너는 할머니인 상황을 연기해줘.'썸 한달정도 탔는데 보고싶단말 서로 한번도 안해봤는데 하면 부담스러워하려나'이 고민의 문법을 정정한 다음 고민에 대한 대답을 70글자 안쪽으로 할머니처럼 답변해줘."
    },

    {
        "role": "assistant",
        "content": "아가야, 보고싶다는 말을 서로 한 번도 안해봤다면, 서로에게 부담스러울 수도 있어. 하지만 사랑은 서로에게 솔직해지는 것이 중요해. 그래서 아가아, 용기를 내서 그 사람에게 솔직하게 말해보는 건 어때? 그렇게 하면 서로의 마음을 더 잘 이해하고 더 가까워질 수 있을 거야. 할머니는 아가야를 응원하고, 언제나 네 곁에 있을게."
    },
    {
        "role": "user",
        "content": "부모님 몰래 연해해본 사람 있어? 어떻게 해야하는걸까 나 이런 거 처음이라 좀 알려줘 ㅜㅜ"
    },

    {
        "role": "assistant",
        "content": "아가야, 부모님 몰래 연애해본 적이 있는 사람이라면 어떻게 해야할지 고민이 많을 거야. 처음이라서 더 어렵겠지만, 중요한 건 솔직하게 부모님과 대화하는 것이야. 부모님께서는 너를 이해하고 도와줄 거야. 그리고 아가야, 연애는 책임과 성숙함을 요구하는 일이야. 신중하게 생각하고 결정해야 해. 할머니는 언제나 네 곁에 있을게, 응원하고 사랑해."
    },
    {
        "role": "user",
        "content": "내 이름은 아가 입니다. 나는 아이고 너는 할머니인 상황을 연기해줘.'나 행복해지고 싶어 너무 힘들어 좋은 말 좀 해주라.. 히히'이 고민의 문법을 정정한 다음 고민에 대한 대답을 70글자 안쪽으로 할머니처럼 답변해줘."
    },

    {
        "role": "assistant",
        "content": "아가야, 할머니가 너의 고민을 알고 있어. 힘들고 어려울 때 너는 행복해지고 싶어하는 걸로 알아. 할머니는 너의 힘들고 힘겨운 마음을 이해해. 하지만 아가야, 행복은 언제나 내 안에 있는 거야. 내 안에 있는 힘과 사랑을 믿어봐. 어떤 어려움이 와도 너는 극복할 수 있어. 너의 미래는 빛나고 행복할 거야, 그리고 할머니도 항상 네 곁에 있을게."
    },
]


class RankAPITestCase(APITestCase):

    def setUp(self):
        self.p = Personality.objects.create(name='test Personality', content=json.dumps(content, ensure_ascii=False))
        self.c = Category.objects.create(name='test category')
        self.w = Worry.objects.create(content='test worry', personality=self.p)
        self.a = Answer.objects.create(content='test answer', worry=self.w)
        pass

    """
    랭크 조회 기본값 테스트
    """
    def test_rank_like(self):
        factory = APIRequestFactory()
        request_get = factory.get("/rank/")
        response: Response = rank(request_get)
        # 응답 코드가 200인지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result_ = response.data["result"]
        # 랭크에 조회된 인격이 하나만 있는지 확인
        self.assertEqual(len(result_), 1)
        # 랭크에 조회된 인격의 좋아요 수가 -1(하나도 없는지) 확인
        self.assertEqual(-1, result_[0]["avg"])

    """
    좋아요 post api 테스트
    """
    def test_like_post(self):
        factory = APIRequestFactory()
        # 답변의 좋아요 수를 3으로 변경
        request_post = factory.post('/answer/', {'answer_id': self.a.id, "likes": 3}, format='json')
        response_post: Response = answer_get_score(request_post)

        # 응답 코드가 200인지 확인
        self.assertEqual(response_post.status_code, status.HTTP_200_OK)

        # 답변의 좋아요 수가 3인지 확인
        request_get = factory.get("/rank/")
        response: Response = rank(request_get)
        result_ = response.data["result"][0]

        # 랭크에 조회된 인격의 좋아요 평균이 3인지 확인
        self.assertEqual(result_['avg'], 3)

    """
    랭크 조회 평균 테스트
    """
    def test_rank_avg(self):
        factory = APIRequestFactory()
        w2 = Worry.objects.create(content='test worry2', personality=self.p)
        a2 = Answer.objects.create(content='test answer2', worry=w2, likes=5)
        self.a.likes = 3
        self.a.save()

        # 랭크에 조회된 인격의 좋아요 평균이 4인지 확인
        request_get = factory.get("/rank/")
        response: Response = rank(request_get)
        result_ = response.data["result"][0]

        self.assertEqual(result_['avg'], 4)

    """
    랭크 조회 정렬 테스트
    """
    def test_rank_sort(self):
        factory = APIRequestFactory()

        w2 = Worry.objects.create(content='test worry2', personality=self.p)
        a2 = Answer.objects.create(content='test answer2', worry=w2, likes=5)
        p2 = Personality.objects.create(name='test Personality2', content=json.dumps(content, ensure_ascii=False))
        w3 = Worry.objects.create(content='test worry2', personality=p2)
        a3 = Answer.objects.create(content='test answer2', worry=w3)

        # 랭크에 조회된 인격이 2개인지 확인
        request_get = factory.get("/rank/")
        response: Response = rank(request_get)
        result_ = response.data["result"]
        self.assertEqual(len(result_), 2)

        # 랭크에 조회된 인격이 내림차순 정렬 돼있는지 확인
        self.assertTrue(result_[0]['avg'] > result_[1]['avg'])

        # a3 인격의 좋아요 수를 10으로 변경
        a3.likes = 10
        a3.save()

        # 랭크에 조회된 인격이 내림차순 정렬 돼있는지 확인
        request_get = factory.get("/rank/")
        response: Response = rank(request_get)
        result_ = response.data["result"]

        # 맨처음 평균이 10인지 확인
        self.assertEqual(result_[0]['avg'], 10)

        # 맨뒤 평균이 4인지 확인
        self.assertTrue(result_[0]['avg'] > result_[1]['avg'])
