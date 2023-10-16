from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


# 헬퍼 클래스 - 유저를 생성할 때 사용
class UserManager(BaseUserManager):    
    def create_user(self, account_id, user_name, tiiun_number, garden_size, address, password, **kwargs):
        """
        주어진 id, name(별명), 비밀번호 개인정보로 User 인스턴스 생성
        """        
        if not account_id:
            raise ValueError('아이디는 필수 항목입니다.')
        if not user_name:
            raise ValueError('이름은 필수 항목입니다.')
        if not tiiun_number:
            raise ValueError('틔운 제품키를 작성해주세요.')
        if not garden_size:
            raise ValueError('화단 크기를 선택해주세요.')
        if not address:
            raise ValueError('주소는 필수 항목입니다.')
        if not password:
            raise ValueError('비밀번호는 필수 항목입니다.')
        
        user = self.model(
            account_id=account_id,
            user_name=user_name,
            tiiun_number=tiiun_number,
            garden_size=garden_size,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, account_id=None, user_name=None, tiiun_number=None, garden_size=None, address=None, password=None, **extra_fields):
        """
        주어진 id, name(별명), 비밀번호 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(
            account_id=account_id,
            user_name=user_name,
            tiiun_number=tiiun_number,
            garden_size=garden_size,
            address=address,
            password=password,
        )
        
        superuser.is_active = True # 해당 계정이 활성인지를 결정
        superuser.is_staff = True # 참인 경우 admin 사이트에 접속 가능
        superuser.is_superuser = True # 모든 권한 부여
        
        superuser.save(using=self._db)
        return superuser
    
    
# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):    
    # 입력하는 정보
    account_id = models.CharField(max_length=30, unique=True, null=False, blank=False) # 아이디
    user_name = models.CharField(max_length=30, null=False, blank=False) # 이름
    tiiun_number = models.CharField(max_length=30, null=False, blank=False) # 틔운 제품키
    garden_size = models.CharField(max_length=1, null=False, blank=False) # 화단 크기
    address = models.CharField(max_length=30, null=False, blank=False) # 주소
    
    # 자동으로 입력되는 정보
    date_joined = models.DateTimeField(_('created_at'), auto_now_add=True)
    date_updated = models.DateTimeField(_('updated_at'), auto_now=True)
    
    # 권한 관련
    is_active = models.BooleanField(_('active_status'), default=True)
    is_staff = models.BooleanField(_('staff_status'), default=False)
    is_superuser = models.BooleanField(_('superuser_status'), default=False)
    
    USERNAME_FIELD = 'account_id' # 유저 모델의 unique=True가 옵션으로 설정된 필드 값
    REQUIRED_FIELDS = ['user_name', 'tiiun_number', 'garden_size', 'address'] # 필수로 받고 싶은 값
    
    # 헬퍼 클래스 사용
    objects = UserManager()