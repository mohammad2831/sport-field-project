from.models import UserCategoryScore , AnonymousUserProfile
from django.db.models import Sum
from django.db import transaction 




def recommendation(session_key: str):

    try:
        user_category_scores_queryset = UserCategoryScore.objects.filter(session_key=session_key)
        
        if not user_category_scores_queryset.exists():
            return {'error': 'No category scores found for this session.', 'recommended_sports': []}
        
       
        anonymous_profile = AnonymousUserProfile.objects.filter(session_key=session_key).first()
        if not anonymous_profile:
             return {'error': 'User profile not found for this session.', 'recommended_sports': []}
        

        user_age = anonymous_profile.age if anonymous_profile.age is not None else None
        

        categories_group1 = {'2', '3', '4', '5', '6', '7'}
        categories_group2 = {'8','9','10','11','12','13'}





        sum_group1_result = user_category_scores_queryset.filter(
            category__in=categories_group1
        ).aggregate(total_sum=Sum('score'))
        total_score_group1: float = float(sum_group1_result.get('total_sum') or 0) 

        sum_group2_result = user_category_scores_queryset.filter(
            category__in=categories_group2
        ).aggregate(total_sum=Sum('score'))
        total_score_group2: float = float(sum_group2_result.get('total_sum') or 0) 

        avg_group1= total_score_group1 / 6
        avg_group2= total_score_group2 / 6

        
        with transaction.atomic(): 
            deleted_profiles_count, _ = AnonymousUserProfile.objects.filter(session_key=session_key).delete()
            deleted_scores_count, _ = UserCategoryScore.objects.filter(session_key=session_key).delete()
            print(f"Deleted {deleted_profiles_count} anonymous profiles and {deleted_scores_count} category scores for session {session_key}.")
        
        
        if avg_group1 > avg_group2:
            return{
                'sport_recomend': 'فوتسال و شنا'
            }
        elif avg_group1 < avg_group2:
            return{
                'sport_recomend': 'دوومیدانی'
            }
        else:{
            'sport_recomend': 'فوتسال و دوومیدانی'
        }
       
    except Exception as e:
        return {'error': str(e), 'recommended_sports': []}





