import datetime
from mcipc.rcon.je import Biome, Client
from mcipc.query import Client as Client_q

from .models import Script, Code, Config, Profile, User, Command_log

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
import mcipc
#Toolsの定義
def logtext(req,text,st):
    ipadd = req.META.get('REMOTE_ADDR')
    return text+"の実行に"+st+"しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
def logging(text):
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text+"\n")
def get_conf(request):
    configs = None
    configs_list = Config.objects.all()
    for configs in configs_list:
        if configs.user == request.user:
            break
    return configs
#定義終了
def index(request):
    return render(request, 'index.html')

def cline(request):
    con = {'command':request.POST["com"]}
    print(request.POST)
    return render(request,'console.html',con)
@login_required(login_url='/accounts/login/')
def query(request):
    configs = get_conf(request)
    text = 'Query Full Stats'
    try:
        with Client_q(configs.server_ip, int(configs.query_port)) as client:
            full_stats= client.stats(full=True)
            re = "状態を取得しています"
            come = "状態の取得に成功しました"
            error = ""
            he = "成功しました"
        with Client(configs.server_ip, int(configs.rcon_port), passwd='minecraft') as client:
            seed = client.seed
    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        he = str(e)
        seed =""
    except ConnectionResetError as e:
        re = "[Error] Server not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        he = str(e)
        seed =""
    text = 'Query Full Stats'
    try:
        context = {'seed':seed,'query':re,'command': text,'ip':configs.server_ip,'port':25565,'session':full_stats.session_id,"player":full_stats.players,"host":full_stats.host_name,"version":full_stats.version,"map":full_stats.map,"num":full_stats.num_players,"num_max":full_stats.max_players,"port":full_stats.host_port,"ip_host":full_stats.host_ip,"user_name":request.user}
    except UnboundLocalError:
        context = {'query':come,'command': text,'ip':configs.server_ip,'port':25565,'error':error,'error_t':"ConnectionRefusedError"}
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text+come+"\n")
    return render(request,'query.html',context)
@login_required(login_url='/accounts/login/')


def script(request, ids):
    configs = get_conf(request)
    scripts = Script.objects.get(id=ids)
    funcs = scripts.script
    funcs_list = funcs.split("/")
    re ="/ "
    ipadd = request.META.get('REMOTE_ADDR')
    for i in range(len(funcs_list)-1):
        func_du = funcs_list[int(i)+1].split(" ")
        try:
            with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
                re = re+client.run(*func_du)
                re = re+" / "
                text2 = scripts.script_name+"のスクリプトの実行に成功しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
        except ConnectionRefusedError as e:
            text2 = scripts.script_name+"のスクリプトの実行に失敗しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text2+"\n")
    return render(request, 'script.html', {'script_field': funcs,'script':scripts,'debug':len(funcs_list),'re':re,"user_name":request.user})
def code(request, ids):
    scripts = Code.objects.get(id=ids)
    funcs = scripts.code
    stats = scripts.selecter
    every = scripts.condition
    funcs_list = funcs.split("/")
    if stats == "1":
        stats_ = "active"
    else:
        stats_ = "inactive"
        
    re ="コード "+scripts.script_name+" の設定を "+stats_+" にしました。"+"中身のコードは "+funcs+"　で、 "+every+" 秒おきに実行します。"
    ipadd = request.META.get('REMOTE_ADDR')
    with open("code"+str(ids)+".txt","w",encoding="UTF-8") as f:
        f.write(stats+"\n"+funcs+"\n"+every)
    return render(request, 'code.html', {'script_field': funcs,'script':scripts,'debug':len(funcs_list),'re':re,"user_name":request.user})
@login_required(login_url='/accounts/login/')
def scriptindex(request):
    latest_question_list = Script.objects.all()
    template = loader.get_template('scriptindex.html')
    test = list()
    for i in range(len(latest_question_list)):
        test.append(latest_question_list[i])
    context = {
        'latest_question_list': latest_question_list,"user_name":request.user
    }
    return HttpResponse(template.render(context, request))
def codeindex(request):
    latest_question_list = Code.objects.all()
    template = loader.get_template('codeindex.html')
    test = list()
    for i in range(len(latest_question_list)):
        test.append(latest_question_list[i])
    context = {
        'latest_question_list': latest_question_list,"user_name":request.user
    }
    return HttpResponse(template.render(context, request))
@login_required(login_url='/accounts/login/')
def profileac(request):
    configs = get_conf(request)
    return render(request, 'profileac.html',{'user_name':request.user,'config_name':configs.server_name,'ip':configs.server_ip,'rcon_port':configs.rcon_port,'query_port':configs.query_port,'passw':configs.passw})

@login_required(login_url='/accounts/login/')
def console(request):
    configs = get_conf(request)

    re = ""
    text = ""
    if request.method == "POST":
        text = request.POST.get('command')
    if not text:
        pass
    else:
        chat_flag = False #チャットであるかのフラグ
        if not text[0] == "/":
            func_du = ["say"]
            func_du.append(text)
            re = "say "+text
            chat_flag = True
        funcs_list = text.split("/")
        for i in range(len(funcs_list)-1):
            func_du = funcs_list[int(i)+1].split(" ")
        
        try:
            with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
                if not chat_flag:
                    re = client.run(*func_du)
                else:
                    client.run(*func_du)

                text2 = logtext(request,text,"成功")
        except ConnectionRefusedError as e:
            text2 = logtext(request,text,"失敗")
            re = 'ServerNotFoundError'
        except mcipc.rcon.errors.NoPlayerFound as e:
            text2 = logtext(request,text,"失敗")
            re = 'NoPlayerFoundError'
        except UnboundLocalError:
            text2 = logtext(request,text,"失敗")
            re = 'SyntaxError'
        with open("log.txt","a",encoding="UTF-8") as f:
            f.write(text2+"\n")
        command = Command_log(command_text=text,return_text=re,user=request.user,time=datetime.datetime.now())
        command.save()
    latest_question_list = Command_log.objects.all()
    template = loader.get_template('console2.html')
    test = list()
    #適合するユーザーの履歴を取得
    for i in range(len(latest_question_list)):
        if latest_question_list[i].user == request.user:
            test.append(latest_question_list[i])
    test.reverse()
    for i in latest_question_list:
        i.time = str(i.time).replace("年","/")
        i.time = str(i.time).replace("月","/")
        i.time = str(i.time).replace("日","")
        i.time = str(i.time).replace("+"," ")
    context = {
        'latest_question_list': test[0:4],"user_name":request.user
    }
    return HttpResponse(template.render(context, request))
@login_required(login_url='/accounts/login/')
def config_page(request):
    name = ""
    if request.method == "POST":
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        qport = request.POST.get('qport')
        rport = request.POST.get('rport')
    if not name:
        pass
    else:
        configs_list = Config.objects.all()
        for configs in configs_list:
            if configs.user == request.user:
                break
        configs.delete()
        config_data = Config(server_name=name,user=request.user,server_ip=ip,rcon_port=rport,query_port=qport)
        config_data.save()
    context = {'user_name':request.user}
    template = loader.get_template('config_page.html')
    return HttpResponse(template.render(context,request))

def help(request):
    context = {'user_name':request.user}
    template = loader.get_template('helppage.html')
    return HttpResponse(template.render(context,request))