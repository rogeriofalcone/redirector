from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser


class RoleMemberManager(models.Manager):
    def get_roles_for_member(self, member_obj):
        if isinstance(member_obj, AnonymousUser):
            # Anonymous users can have roles, yet
            return []
            
        member_type = ContentType.objects.get_for_model(member_obj)
        return [role_member.role for role_member in self.model.objects.filter(member_type=member_type, member_id=member_obj.pk)]


class PermissionManager(models.Manager):
    def get_for_holder(self, holder):
        ct = ContentType.objects.get_for_model(holder)
        return self.model.objects.filter(permissionholder__holder_type=ct).filter(permissionholder__holder_id=holder.pk)
