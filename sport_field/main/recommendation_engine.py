from.models import UserCategoryScore , AnonymousUserProfile, ResultUser
from django.db.models import Sum
from django.db import transaction 
from datetime import datetime

def recommendation(session_key: str):

    try:
        user_category_scores_queryset = UserCategoryScore.objects.filter(session_key=session_key)
        
        if not user_category_scores_queryset.exists():
            return {'error': 'No category scores found for this session.', 'recommended_sports': []}
        
       
        anonymous_profile = AnonymousUserProfile.objects.filter(session_key=session_key).first()
        if not anonymous_profile:
             return {'error': 'User profile not found for this session.', 'recommended_sports': []}
        

        user_age = anonymous_profile.age if anonymous_profile.age is not None else None
        user_name = anonymous_profile.full_name
        time = datetime.now()

        categories_group1 = {'2', '3', '4', '5', '6' }
        categories_group2 = {'7','8','9','10','11'}
        #add 12 and 13 after fix db





        sum_group1_result = user_category_scores_queryset.filter(
            category__in=categories_group1
        ).aggregate(total_sum=Sum('score'))
        total_score_group1: float = float(sum_group1_result.get('total_sum') or 0) 

        sum_group2_result = user_category_scores_queryset.filter(
            category__in=categories_group2
        ).aggregate(total_sum=Sum('score'))
        total_score_group2: float = float(sum_group2_result.get('total_sum') or 0) 

        avg_group1 = total_score_group1 / len(categories_group1) if len(categories_group1) > 0 else 0
        avg_group2 = total_score_group2 / len(categories_group2) if len(categories_group2) > 0 else 0
        
        
        
        if avg_group1 > avg_group2:
                
            sport_recomended= 'فوتسال و شنا'
            
        elif avg_group1 < avg_group2:
                
            sport_recomended= 'دو و میدانی'
            
        else:
            sport_recomended= 'فوتسال و دوومیدانی'
        
       

        with transaction.atomic():
            ResultUser.objects.create(
                full_name=user_name,
                age=user_age,
                result=sport_recomended,
                time=time
            )
            deleted_profiles_count, _ = AnonymousUserProfile.objects.filter(session_key=session_key).delete()
            deleted_scores_count, _ = UserCategoryScore.objects.filter(session_key=session_key).delete()

        return {
            'sport_recomend': sport_recomended
        }

    except Exception as e:
        return {'error': str(e), 'recommended_sports': []}




