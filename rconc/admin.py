from django.contrib import admin

from .models import Command_log, Script, Config

class ConfigAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Configuration",{"fields":['server_name','user']}),
        ("ServerSettings",{"fields":['server_ip','rcon_port','query_port','passw','active']}),
    ]
    list_display = ('id','server_name','server_ip','rcon_port','query_port')
    search_fields = ('server_name', 'server_ip')
    save_as = True
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('id','script_name','script')
    search_fields = ('script_name', 'script')
admin.site.register(Script,ScriptAdmin)
admin.site.register(Config,ConfigAdmin)
admin.site.register(Command_log)