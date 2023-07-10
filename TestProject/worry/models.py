from django.db import models

# Create your models here.
class Worry(models.Model): # Worry 모델
    # TODO: 유저 모델을 연결해야함(FK)
    # TODO: 카테고리 모델을 연결해야함(FK)
    # TODO: 인격 모델을 연결해야함(FK)
    # TODO: 답변 모델을 연결해야함(FK)
    content = models.TextField() # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    modified_at = models.DateTimeField(auto_now=True) # 수정일
    deleted_at = models.DateTimeField(null=True, blank=True) # 삭제일
    
    def __str__(self):
        return self.content
    
class Answer(models.Model): # Answer 모델
    worry = models.ForeignKey(Worry, on_delete=models.CASCADE) # Worry 모델과 1:1 관계
    content = models.CharField(max_length=300) # GPT가 답변한 내용