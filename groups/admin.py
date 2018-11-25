from django.contrib import admin
from groups.models import Group, GroupMember

# puts group members on the same page as the groups page for easy editing
class GroupMemberInline(admin.TabularInline):
	model = GroupMember

admin.site.register(Group)

# Register your models here.
