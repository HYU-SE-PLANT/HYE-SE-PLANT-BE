from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


# Create your models here.
# 헬퍼 클래스 - 유저를 생성할 때 사용
class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, account_id, user_name, password, **kwargs):
        """
        주어진 id, name(별명), 비밀번호 개인정보로 User 인스턴스 생성
        """
        if (not account_id) or (not user_name):
            raise ValueError('Users must type both account_id and user_name')
        user = self.model(
            account_id=account_id,
            user_name=user_name,
        )
        hashed_password = make_password(password)
        user.set_password(hashed_password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, account_id=None, user_name=None, password=None, **extra_fields):
        """
        주어진 id, name(별명), 비밀번호 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(
            account_id=account_id,
            user_name=user_name,
            password=password
        )
        superuser.is_active = True # 해당 계정이 활성인지를 결정
        superuser.is_staff = True # 참인 경우 admin 사이트에 접속 가능
        superuser.is_superuser = True # 모든 권한 부여
        superuser.save(using=self._db)
        return superuser
    
    
# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    # 헬퍼 클래스 사용
    objects = UserManager()
    
    account_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
    user_name = models.CharField(max_length=30, null=False, blank=False)
    date_joined = models.DateTimeField(_('created_at'), default=timezone.now)
    is_active = models.BooleanField(_('active_status'), default=True)
    is_staff = models.BooleanField(_('staff_status'), default=False)
    is_superuser = models.BooleanField(_('superuser_status'), default=False)
    
    USERNAME_FIELD = 'account_id' # 유저 모델의 unique=True가 옵션으로 설정된 필드 값
    REQUIRED_FIELDS = ['user_name'] # 필수로 받고 싶은 값