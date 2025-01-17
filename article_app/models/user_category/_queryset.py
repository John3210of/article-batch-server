from django.db import models

class UserCategoryQuerySet(models.QuerySet):
    def get_active_user_category(self, user_id:int):
        return self.filter(user_id=user_id, is_activated=True)