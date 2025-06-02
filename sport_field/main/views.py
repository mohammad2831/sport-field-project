from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnonymousUserProfileSerializer, QuestionSerializer
from .models import AnonymousUserProfile, Question, Answer


class InfoOneView(APIView):
    def get(self, request):
        print("hi this a test")
        return Response("hi")
    


class PersonalInfoView(APIView):
    def post(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            request.session.save() 
            session_key = request.session.session_key
        
    
        serializer = AnonymousUserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            age_input = serializer.validated_data.get('age')
            profile, created = AnonymousUserProfile.objects.update_or_create(
                session_key=session_key,
                defaults={
                    'age': age_input,
                  
                }
            )

            initial_questions = Question.objects.filter(category='مشخصات شخصی').prefetch_related('answers')
           
            question_serializer = QuestionSerializer(initial_questions, many=True)

            # 5. ارسال پاسخ به PWA
            return Response({
                'message': 'Profile saved and quiz started successfully.',
                'session_id': session_key, 
                'initial_questions': question_serializer.data
            }, status=status.HTTP_200_OK)
        else:
           
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

