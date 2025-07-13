from rest_framework import serializers
from .models import SportFields, Question, Answer, AnonymousUserProfile , UserCategoryScore

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
    full_name = serializers.CharField(required = True)
    
    class Meta:
        model = AnonymousUserProfile
        fields = ['age','full_name'] 
                                                      

class Question2ViewSerializer(serializers.Serializer):
    
    category = serializers.IntegerField(required=True)
    score = serializers.FloatField(required=True)



class UserCategoryScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategoryScore
        fields = ['category', 'score'] 
        