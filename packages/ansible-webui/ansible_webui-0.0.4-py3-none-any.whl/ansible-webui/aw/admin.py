from django.contrib import admin

from aw.models import Job, JobExecution, \
    JobPermission, JobPermissionMemberUser, JobPermissionMemberGroup, JobPermissionMapping, \
    JobExecutionResult, JobError, AwAPIKey

admin.site.register(Job)
admin.site.register(JobExecution)
admin.site.register(JobPermission)
admin.site.register(JobPermissionMemberUser)
admin.site.register(JobPermissionMemberGroup)
admin.site.register(JobPermissionMapping)
admin.site.register(JobExecutionResult)
admin.site.register(JobError)
admin.site.register(AwAPIKey)
