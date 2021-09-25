from django.shortcuts import get_object_or_404, render
import datetime
from mcipc.rcon.je import Biome, Client
from django.http import HttpResponse
from mcipc.query import Client as Client_q
from .models import Script, Code, Config, Profile
from django.template import loader
from django.contrib.auth.decorators import login_required
import mcipc
from django.utils import timezone
#from tools import *
#Toolsの定義
def logtext(req,text,st):
    ipadd = req.META.get('REMOTE_ADDR')
    return text+"の実行に"+st+"しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
def logging(text):
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text+"\n")
#定義終了
ip = '127.0.0.1'
port =  25575
def index(request):
    return render(request, 'index.html')

def cline(request):
    con = {'command':request.POST["com"]}
    print(request.POST)
    return render(request,'console.html',con)

def query(request):
    maxint= Config.objects.count()
    configs = None
    num = 0
    for i in range(1,maxint+1):
        configs = Config.objects.get(id=int(i))
        if configs.user == request.user:
            num = i
            break
    text = 'Query Full Stats'
    try:
        with Client_q(configs.server_ip, int(configs.query_port)) as client:
            full_stats= client.stats(full=True)
            re = "状態を取得しています"
            come = "状態の取得に失敗しました"
            error = ""
            he = "成功しました"
        with Client(ip, port, passwd='minecraft') as client:
            seed = client.seed
        #context = {'query':come,'command': text,'ip':ip,'port':25565,'error':error,'error_t':""}
    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        he = str(e)
        seed =""
        #context = {'query':come,'command': text,'ip':ip,'port':25565,'error':error,'error_t':"ConnectionRefusedError"}
    except ConnectionResetError as e:
        re = "[Error] Server not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        he = str(e)
        seed =""
        #context = {'query':come,'command': text,'ip':ip,'port':25565,'error':error,'error_t':"ConnectionResetError"}
    text = 'Query Full Stats'
    context = {'seed':seed,'query':re,'command': text,'ip':ip,'port':25565,'session':full_stats.session_id,"player":full_stats.players,"host":full_stats.host_name,"version":full_stats.version,"map":full_stats.map,"num":full_stats.num_players,"num_max":full_stats.max_players,"port":full_stats.host_port,"ip_host":full_stats.host_ip}
    
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text+come+"\n")
    return render(request,'query.html',context)
@login_required(login_url='/accounts/login/')
def test2(request,type):
    maxint= Config.objects.count()
    configs = None
    num = 0
    for i in range(1,maxint+1):
        configs = Config.objects.get(id=int(i))
        if configs.user == request.user:
            num = i
            break
    text = "/"+type
    ipadd = request.META.get('REMOTE_ADDR')
    try:
        with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
            re = client.run(str(type))
            come = "を実行しました"
            error = ""
            he = "なし"
            text2 = logtext(request,text,"成功")
            context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}
    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "の実行に失敗しました"
        error = str(e)
        he = str(e)
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}
    except mcipc.rcon.errors.NoPlayerFound as e:
        re = "[Error] Player not found"
        come = "の実行に失敗しました"
        error = "プレイヤーが存在しません。"
        he = "プレイヤーが存在しません。"
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}
    logging(text2)
    #context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he, \
    #           'ru':request.user, 'cu':configs.user}
    return render(request,'config.html',context)
@login_required(login_url='/accounts/login/')
def test3(request,type,type2):
    maxint= Config.objects.count()
    configs = None
    num = 0
    for i in range(1,maxint+1):
        configs = Config.objects.get(id=int(i))
        if configs.user == request.user:
            num = i
            break
    text = "/"+type+" "+type2
    come = ""
    ipadd = request.META.get('REMOTE_ADDR')
    try:
        with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
            re = client.run(str(type),str(type2))
            come = "を実行しました"
            error = ""
            he = "なし"
            text2 = logtext(request,text,"成功")
            context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he,'ru':request.user, 'cu':configs.user}

    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "の実行に失敗しました"
        error = str(e)
        he = str(e)
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he,'ru':request.user, 'cu':configs.user}

    except mcipc.rcon.errors.NoPlayerFound as e:
        re = "[Error] Player not found"
        come = "の実行に失敗しました"
        error = "プレイヤーが存在しません。"
        he = "プレイヤーが存在しません。"
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he,'ru':request.user, 'cu':configs.user}

    logging(text2)
    #context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error,":error,"he":he, \
    #           'ru':request.user, 'cu':configs.user}
    return render(request,'config.html',context)
@login_required(login_url='/accounts/login/')
def test4(request,type,type2,type3):
    maxint= Config.objects.count()
    configs = None
    num = 0
    for i in range(1,maxint+1):
        configs = Config.objects.get(id=int(i))
        if configs.user == request.user:
            num = i
            break
    text = "/"+type+" "+type2+" "+type3
    ipadd = request.META.get('REMOTE_ADDR')
    try:
        with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
            re = client.run(str(type),str(type2),str(type3))
            come = "を実行しました"
            error = ""
            he = "なし"
            text2 = logtext(request,text,"成功")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}
    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "の実行に失敗しました"
        error = str(e)
        he = str(e)
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}

    except mcipc.rcon.errors.NoPlayerFound as e:
        re = "[Error] Player not found"
        come = "の実行に失敗しました"
        error = "プレイヤーが存在しません。"
        he = "プレイヤーが存在しません。"
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}
    logging(text2)
    #context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he, \
    #           'ru':request.user, 'cu':configs.user}
    return render(request,'config.html',context)
@login_required(login_url='/accounts/login/')
def test5(request,type,type2,type3,type4):
    maxint= Config.objects.count()
    configs = None
    num = 0
    for i in range(1,maxint+1):
        configs = Config.objects.get(id=int(i))
        if configs.user == request.user:
            num = i
            break
    text = "/"+type+" "+type2+" "+type3+" "+type4
    ipadd = request.META.get('REMOTE_ADDR')
    try:
        with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
            re = client.run(str(type),str(type2),str(type3),str(type4))
            come = "を実行しました"
            error = ""
            he = "なし"
            text2 = logtext(request,text,"成功")
            context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}

    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "の実行に失敗しました"
        error = str(e)
        he = str(e)
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}

    except mcipc.rcon.errors.NoPlayerFound as e:
        re = "[Error] Player not found"
        come = "の実行に失敗しました"
        error = "プレイヤーが存在しません。"
        he = "プレイヤーが存在しません。"
        text2 = logtext(request,text,"失敗")
        context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"comment":come,"error":error,"he":he,'ru':request.user, 'cu':configs.user}
    
    logging(text2)
    #context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he, \
    #           'ru':request.user, 'cu':configs.user}
    return render(request,'config.html',context)
@login_required(login_url='/accounts/login/')
def server_op(request,type,type2):
    maxint= Config.objects.count()
    configs = None
    num = 0
    for i in range(1,maxint+1):
        configs = Config.objects.get(id=int(i))
        if configs.user == request.user:
            num = i
            break
    text = "/"+type+" "+type2
    ipadd = request.META.get('REMOTE_ADDR') 
    try:
        with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
            re = client.run(str(type),str(type2))
            come = "を実行しました"
            error = ""
            he = "なし"
            text2 = logtext(request,text,"成功")
    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "の実行に失敗しました"
        error = str(e)
        he = str(e)
        text2 = logtext(request,text,"失敗")
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text2+"\n")
    context = {'command': text,'ip':configs.server_ip,'port':configs.rcon_port,'return':re,"come":come,"error,":error,"he":he, \
               'ru':request.user, 'cu':configs.user}
    return render(request,'config.html',context)
def hennkann(request):
    return render(request,'hennkann.html')

def script(request, ids):
    scripts = Script.objects.get(id=ids)
    funcs = scripts.script
    funcs_list = funcs.split("/")
    re ="/ "
    ipadd = request.META.get('REMOTE_ADDR')
    for i in range(len(funcs_list)-1):
        func_du = funcs_list[int(i)+1].split(" ")
        try:
            with Client(ip, port, passwd='minecraft') as client:
                re = re+client.run(*func_du)
                re = re+" / "
                text2 = scripts.script_name+"のスクリプトの実行に成功しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
        except ConnectionRefusedError as e:
            text2 = scripts.script_name+"のスクリプトの実行に失敗しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text2+"\n")
    return render(request, 'script.html', {'script_field': funcs,'script':scripts,'debug':len(funcs_list),'re':re})
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
    return render(request, 'code.html', {'script_field': funcs,'script':scripts,'debug':len(funcs_list),'re':re})
def profile(request, ids):
    scripts = Profile.objects.get(id=ids)
    funcs = scripts.script
    funcs_list = funcs.split("/")
    re ="/ "
    ipadd = request.META.get('REMOTE_ADDR')
    if scripts.rq == "2":
        text = 'Query Full Stats'
        try:
            with Client_q(scripts.server_ip, int(scripts.query_port)) as client:
                full_stats= client.stats(full=True)
                re = "状態を取得しています"
                come = "状態の取得に失敗しました"
                error = ""
                he = "成功しました"
            with Client(ip, port, passwd='minecraft') as client:
                seed = client.seed
            context = {'seed':seed,'query':re,'command': text,'ip':ip,'port':25565,'session':full_stats.session_id,"player":full_stats.players,"host":full_stats.host_name,"version":full_stats.version,"map":full_stats.map,"num":full_stats.num_players,"num_max":full_stats.max_players,"port":full_stats.host_port,"ip_host":full_stats.host_ip}

        except ConnectionRefusedError as e:
            re = "[Error] Server not found"
            come = "状態の取得に失敗しました"
            error = str(e)
            he = str(e)
            seed =""
            context = {'query':re,'command': text,'ip':ip,'port':25565,'error':error,'error_t':"ConnectionRefusedError"}
        except ConnectionResetError as e:
            re = "[Error] Server not found"
            come = "状態の取得に失敗しました"
            error = str(e)
            he = str(e)
            seed =""
            context = {'query':come,'command': text,'ip':ip,'port':25565,'error':error,'error_t':"ConnectionResetError"}
        with open("log.txt","a",encoding="UTF-8") as f:
            f.write(text+come+"\n")
        return render(request, 'query.html', context)
    elif scripts.rq == "1":
        for i in range(len(funcs_list)-1):
            func_du = funcs_list[int(i)+1].split(" ")
            try:
                with Client(ip, port, passwd='minecraft') as client:
                    re = re+client.run(*func_du)
                    re = re+" / "
                    text2 = scripts.profile_name+"のプロファイルの実行に成功しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
            except ConnectionRefusedError as e:
                text2 = scripts.profile_name+"のプロファイルの実行に失敗しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
            with open("log.txt","a",encoding="UTF-8") as f:
                f.write(text2+"\n")
        return render(request, 'profile.html', {'script_field': funcs,'script':scripts,'debug':len(funcs_list),'re':re})
def scriptindex(request):
    latest_question_list = Script.objects.all()
    template = loader.get_template('scriptindex.html')
    test = list()
    for i in range(len(latest_question_list)):
        test.append(latest_question_list[i])
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))
def codeindex(request):
    latest_question_list = Code.objects.all()
    template = loader.get_template('codeindex.html')
    test = list()
    for i in range(len(latest_question_list)):
        test.append(latest_question_list[i])
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))

def profileindex(request):
    latest_question_list = Profile.objects.all()
    template = loader.get_template('profileindex.html')
    test = list()
    for i in range(len(latest_question_list)):
        test.append(latest_question_list[i])
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))
