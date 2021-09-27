from django.contrib import admin

from .models import Command_log, Script, Config, Profile

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Configuration",{"fields":['profile_name','user']}),
        ("ServerSettings",{"fields":['server_ip','rcon_port','query_port','passw']}),
        ("Rcon/Query",{"fields":['rq','script']})
    ]
    list_display = ('id','profile_name','server_ip','rq')
    search_fields = ('profile_name', 'script')
    list_filter = ['rq']
class ConfigAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Configuration",{"fields":['server_name','user']}),
        ("ServerSettings",{"fields":['server_ip','rcon_port','query_port','passw']}),
    ]
    list_display = ('id','server_name','server_ip','rcon_port','query_port')
    search_fields = ('server_name', 'server_ip')
    save_as = True
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('id','script_name','script')
    search_fields = ('script_name', 'script')
admin.site.register(Script,ScriptAdmin)
admin.site.register(Config,ConfigAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Command_log)