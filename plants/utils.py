from django.utils import timezone


# is_harvested 를 결정하는 함수
def determine_is_harvested(harvested_at):
    """
    날짜가 제공되면 True, 그렇지 않으면 False를 반환한다.
    """
    return harvested_at is not None


# growth_level을 결정하는 함수
def calculate_growth_level(plant_type, planted_at):
    """
    planted_at으로부터 오늘까지의 날짜를 계산해서
    발아기(germination), 성장기(growth), 수확기(harvest) 단계를 반환한다.
    모든 경우가 아닐 경우, 비활성기(nothing)을 반환한다.
    """
    today = timezone.now().date()
    days_since_planted = (today - planted_at.date()).days
    
    if plant_type.germination_period_start <= days_since_planted <= plant_type.germination_period_end:
            return 'germination'
    elif plant_type.growth_period_start <= days_since_planted <= plant_type.growth_period_end:
        return 'growth'
    elif plant_type.harvest_period_start <= days_since_planted <= plant_type.harvest_period_end:
        return 'harvest'
    else:
        return 'nothing'
    
    
# 수정하고자 하는 정보가 빈칸인지 확인
def is_blank(data):
    return data.strip() == ''