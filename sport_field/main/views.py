from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnonymousUserProfileSerializer, QuestionSerializer, Question2ViewSerializer, UserCategoryScoreSerializer
from .models import AnonymousUserProfile, Question, Answer, UserCategoryScore
from rest_framework import status
from django.db import transaction 
from django.db import models
from .recommendation_engine import recommendation
from django.db import IntegrityError # <-- IntegrityError را ایمپورت کنید
from django.db.models import Prefetch
class InfoOneView(APIView):
    def get(self, request):
        print("hi this a test")
        return Response("hi")
    


class QuestonInitialView(APIView):
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
            
            initial_questions = Question.objects.filter(category='2',min_age__lte=age_input,  max_age__gte=age_input   
            ).prefetch_related(
                models.Prefetch(
                    'answers',
                    queryset=Answer.objects.filter(age=age_input)  
                )
            )
                
            question_serializer = QuestionSerializer(initial_questions, many=True)

            return Response({
                'category': '2',
                'message': 'Profile saved and quiz started successfully.',
                'session_id': session_key, 
                'initial_questions': question_serializer.data
            }, status=status.HTTP_200_OK)
        else:
           
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class QuestionView(APIView):
    def post(self, request, id_q):
        try:
            id_q = int(id_q)
            if not (2 <= id_q <= 12):
                return Response({'error': 'Invalid category ID. Category must be between 2 and 12.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Category ID must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        session_key = request.session.session_key
        serdata = Question2ViewSerializer(data=request.data)
        if serdata.is_valid():
            category = serdata.validated_data['category']
            score = serdata.validated_data['score']

            try:
                user_profile = AnonymousUserProfile.objects.get(session_key=session_key)
            except AnonymousUserProfile.DoesNotExist:
                return Response({'error': 'User profile not found for this session.'}, status=status.HTTP_404_NOT_FOUND)

            if user_profile.age is not None:
                user_age = user_profile.age
            else:
                return Response({'error': 'User age is not set in the profile.'}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                try:
                    UserCategoryScore.objects.update_or_create(
                        session_key=user_profile,  # استفاده از نمونه user_profile به جای رشته session_key
                        category=category,
                        defaults={'score': score}  # استفاده از defaults برای به‌روزرسانی امتیاز
                    )
                except IntegrityError:
                    print(f"Warning: IntegrityError caught for session {session_key}, category {category}. "
                          "Record likely already exists due to race condition. Continuing...")
                    pass 

            if id_q == 12:
                recommendation_results = recommendation(session_key)
                return Response({
                    'message': recommendation_results,
                }, status=status.HTTP_200_OK)
            else:
                next_questions = Question.objects.filter(
                    category=id_q + 1,
                    min_age__lte=user_age,
                    max_age__gte=user_age
                ).prefetch_related(
                    models.Prefetch(
                        'answers',
                        queryset=Answer.objects.filter(age=user_age)
                    )
                )
                    
                question_serializer = QuestionSerializer(next_questions, many=True)

                return Response({
                    'category': str(id_q + 1),
                    'session_id': session_key,
                    'next_questions': question_serializer.data
                }, status=status.HTTP_200_OK)
        else:
            return Response(serdata.errors, status=status.HTTP_400_BAD_REQUEST)







































"""
class QuestionFinnalView(APIView):
    def post(self, request):
        session_key = request.session.session_key

        serdata = Question2ViewSerializer(data=request.data)
        if serdata.is_valid():
            
            category = serdata.validated_data['category']
            score = serdata.validated_data['score']

            try:   
                user_profile = AnonymousUserProfile.objects.get(session_key=session_key)
            except AnonymousUserProfile.DoesNotExist:
                return Response({'error': 'User profile not found for this session.'}, status=status.HTTP_404_NOT_FOUND)

            if user_profile.age is not None:
                user_age = user_profile.age
            else:
                return Response({'error': 'User age is not set in the profile.'}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic(): 
                    UserCategoryScore.objects.update_or_create(
                        session_key=session_key,
                        category=category,
                        score=score
                    )


            recommendation_results = recommendation(session_key)

            return Response({
                'message': recommendation_results
                ##'all_user_category_scores': scores_serializer.data, # تمامی امتیازات دسته‌بندی‌ها
                
            }, status=status.HTTP_200_OK)

        else:
            return Response(serdata.errors, status=status.HTTP_400_BAD_REQUEST)






   """        





































class Question3View(APIView):
    def post(self, request):
        pass




"""
class SubmitResponsesAPIView(APIView):

    def post(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            return Response({'error': 'Session not found. Please enable cookies.'}, status=status.HTTP_400_BAD_REQUEST)

        responses_data = request.data.get('responses', [])
        next_category_name = request.data.get('next_category') 

        if not responses_data:
            return Response({'error': 'No responses provided. Please send at least one response.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for res_data in responses_data:
                    question_id = res_data.get('question_id')
                    
                    if not question_id:
                        raise ValueError("Missing 'question_id' for a response.")

                    try:
                        question = Question.objects.get(id=question_id)
                    except Question.DoesNotExist:
                        raise ValueError(f"Question with ID {question_id} not found.")

                    if question.type == Question.CHOICE:
                        chosen_answer_id = res_data.get('chosen_answer_id')
                        if not chosen_answer_id:
                            raise ValueError(f"Missing 'chosen_answer_id' for choice question ID {question_id}.")
                        try:
                            chosen_answer = Answer.objects.get(id=chosen_answer_id, question=question)
                        except Answer.DoesNotExist:
                            raise ValueError(f"Answer with ID {chosen_answer_id} for question ID {question_id} not found.")

                        UserResponse.objects.update_or_create(
                            session_key=session_key,
                            question=question,
                            defaults={
                                'chosen_answer': chosen_answer,
                                'text_answer': None 
                            }
                        )
                    elif question.type == Question.TEXT:
                        text_answer_content = res_data.get('text_answer', '') 
                        
                        UserResponse.objects.update_or_create(
                            session_key=session_key,
                            question=question,
                            defaults={
                                'text_answer': text_answer_content,
                                'chosen_answer': None 
                            }
                        )
                    else:
                        raise ValueError(f"Unknown question type '{question.type}' for question ID {question_id}.")

            if next_category_name and next_category_name != 'final':
                next_questions = Question.objects.filter(category=next_category_name).prefetch_related('answers').order_by('id')
                
                next_question_data = QuestionSerializer(next_questions, many=True).data

                return Response({
                    'message': 'Responses submitted successfully.',
                    'next_questions': next_question_data,
                    'has_more_questions': True, 
                    'next_category_name': next_category_name 
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'All responses submitted successfully. Ready for recommendation.',
                    'has_more_questions': False,
                    'redirect_to_recommendation': True 
                }, status=status.HTTP_201_CREATED)

        except (ValueError, Question.DoesNotExist, Answer.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An unexpected server error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""