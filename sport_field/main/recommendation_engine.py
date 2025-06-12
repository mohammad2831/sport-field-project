from.models import UserCategoryScore , AnonymousUserProfile
from django.db.models import Sum

def recommendation(session_key: str):

    try:
        user_category_scores_queryset = UserCategoryScore.objects.filter(session_key=session_key)
        
        if not user_category_scores_queryset.exists():
            return {'error': 'No category scores found for this session.', 'recommended_sports': []}
        
       
        anonymous_profile = AnonymousUserProfile.objects.filter(session_key=session_key).first()
        if not anonymous_profile:
             return {'error': 'User profile not found for this session.', 'recommended_sports': []}
        



        user_age = anonymous_profile.age if anonymous_profile.age is not None else None
        

        categories_group1 = {'2', '3', '4', '5', '6'}
        categories_group2 = {'7', '8', '9', '10', '11'}

        sum_group1_result = user_category_scores_queryset.filter(
            category__in=categories_group1
        ).aggregate(total_sum=Sum('score'))
        total_score_group1: float = float(sum_group1_result.get('total_sum') or 0) 

        sum_group2_result = user_category_scores_queryset.filter(
            category__in=categories_group2
        ).aggregate(total_sum=Sum('score'))
        total_score_group2: float = float(sum_group2_result.get('total_sum') or 0) 


        return {
            'total_score_group1': total_score_group1,
            'total_score_group2': total_score_group2,
            'user_age': user_age,
        }
    except Exception as e:
        return {'error': str(e), 'recommended_sports': []}
