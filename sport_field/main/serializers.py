from rest_framework import serializers
from .models import SportFields, Question, Answer, AnonymousUserProfile , UserResponse

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportFields
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'points', 'age']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True) 

    class Meta:
        model = Question
        fields = ['id', 'text', 'category', 'type', 'answers'] 

class AnonymousUserProfileSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=True) 
    
    class Meta:
        model = AnonymousUserProfile
        fields = ['age'] 
                                                      

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['question', 'chosen_answer', 'text_answer'] 