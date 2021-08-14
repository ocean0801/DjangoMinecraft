from django.contrib import admin

from .models import Script, Config, Code, Profile

class CodeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Configuration",{"fields":['script_name','selecter','condition','code']}),
        ("Waring!:これだけでは設定は反映されません！/mine/codeのページで設定を反映するボタンを押さなければなりません。",{"fields":[]})
    ]
    list_display = ('id','script_name','selecter','code')
    search_fields = ('script_name', 'code')
    list_filter = ['selecter']
    actions = ['change_ina_action','change_a_action']
    def change_ina_action(self, request, queryset):  # 引数はこれがデフォルト
        queryset.update(selecter='2')
    change_ina_action.short_description = '状態をinactiveに変更'  # アクションの名前
    def change_a_action(self, request, queryset):  # 引数はこれがデフォルト
        queryset.update(selecter='1')
    change_a_action.short_description = '状態をactiveに変更'  # アクションの名前
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
admin.site.register(Code,CodeAdmin) 
admin.site.register(Config,ConfigAdmin)
admin.site.register(Profile,ProfileAdmin)
