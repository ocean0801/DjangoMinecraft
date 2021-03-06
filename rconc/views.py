import datetime

from mcipc.rcon.je import Client
from mcipc.query import Client as Client_q
from mcipc.rcon.errors import *

from .models import *

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import threading

import time

#Toolsの定義
def logtext(req,text,st):
    "IPアドレスを記録しつつログの文字を作る。"
    ipadd = req.META.get('REMOTE_ADDR')
    return text+"の実行に"+st+"しました。-%s" % datetime.datetime.now() + " on IP" + ipadd
def logging(text):
    """
    ログをとるための関数。
    """
    with open("log.txt","a",encoding="UTF-8") as f:
        f.write(text+"\n")
def get_conf(request):
    configs = None
    configs_list = Config.objects.all()
    for configs in configs_list:
        if configs.user == request.user:
            break
    return configs
def log(text: str, color = ""):
    if color == "red":
        print("\033[31m"+text+"\033[0m")
    elif color == "green":
        print("\033[32m"+text+"\033[0m")
    elif color == "yellow":
        print("\033[33m"+text+"\033[0m")
    elif color == "blue":
        print("\033[34m"+text+"\033[0m")
    elif color == "purple":
        print("\033[35m"+text+"\033[0m")
    elif color == "skyblue":
        print("\033[36m"+text+"\033[0m")
    elif color == "blue":
        print("\033[34m"+text+"\033[0m")
    elif color == "purple":
        print("\033[35m"+text+"\033[0m")
    elif color == "skyblue":
        print("\033[36m"+text+"\033[0m")
    else:
        print(text)
#定義終了
def index(request):
    return render(request, 'index.html')

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
        with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
            seed = client.seed
    except ConnectionRefusedError as e:
        re = "[Error] Server not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        seed =""
    except ConnectionResetError as e:
        re = "[Error] Server not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        seed =""
        
    except AttributeError as e:
        re = "[Error] Conf not found"
        come = "状態の取得に失敗しました"
        error = str(e)
        seed =""
    text = 'Query Full Stats'
    try:
        context = {'seed':seed,'query':re,'command': text,'ip':configs.server_ip,'port':configs.query_port,'session':full_stats.session_id,"player":full_stats.players,"host":full_stats.host_name,"version":full_stats.version,"map":full_stats.map,"num":full_stats.num_players,"num_max":full_stats.max_players,"port":full_stats.host_port,"ip_host":full_stats.host_ip,"user_name":request.user}
    except UnboundLocalError:
        context = {'query':come,'command': text,'ip':configs.server_ip,'port':25565,'error':error,'error_t':"ConnectionRefusedError"}
    except AttributeError:
        context = {'query':come,'command': text,'error':re,'error_t':"AttributeError",'ip':'emply','port':'emply'}
    logging(text+come)
    return render(request,'query.html',context)

@login_required(login_url='/accounts/login/')
def script(request, ids):
    configs = get_conf(request)
    scripts = Script.objects.get(id=ids)
    funcs = scripts.script
    funcs_list = funcs.split("/")
    re ="/ "
    text2 = ""
    for i in range(len(funcs_list)-1):
        func_du = funcs_list[int(i)+1].split(" ")
        text = scripts.script_name
        try:
            with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
                re = re+client.run(*func_du)
                re = re+" / "
                text2 = logtext(request,text,"失敗")
        except ConnectionRefusedError as e:
            text2 = logtext(request,text,"失敗")
            re = re + 'ServerNotFoundError / '
        except ConnectionResetError as e:
            text2 = logtext(request,text,"失敗")
            re = re + 'ServerNotFoundError / '
        except NoPlayerFound as e:
            text2 = logtext(request,text,"失敗")
            re = re + 'NoPlayerFoundError / '
        except UnboundLocalError:
            text2 = logtext(request,text,"失敗")
            re = re + 'SyntaxError / '
        except UnknownCommand:
            text2 = logtext(request,text,"失敗")
            re = re + 'Unknown or incomplete command / '
        except InvalidArgument:
            text2 = logtext(request,text,"失敗")
            re = re + 'InvalidArgument / '
        except LocationNotFound:
            text2 = logtext(request,text,"失敗")
            re = re + 'Location could not be found. / '
    logging(text2)
    return render(request, 'script.html', {'script_field': funcs,'script':scripts,'debug':len(funcs_list),'re':re,"user_name":request.user})
@login_required(login_url='/accounts/login/')
def script_page(request):
    name = ""
    if request.method == "POST":
        name = request.POST.get('name')
        command = request.POST.get('com')
        if not name:
            pass
        else:
            config_data = Script(script_name=name,script=command)
            config_data.save()
            return redirect('/mine/script')
    context = {'user_name':request.user}
    template = loader.get_template('script_page.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/accounts/login/')
def script_do(request,id,type):
    if type == "delete":
        scripts = Script.objects.get(id=id)
        scripts.delete()
    return redirect('/mine/script')
def script_edit(request,id):
    name = ""
    scripts = Script.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        command = request.POST.get('com')
        if not name:
            pass
        else:
            print("POST")
            config_data = Script.objects.get(id=id)
            config_data.script_name = name
            config_data.script = command
            print(command)
            config_data.save()
            return redirect('/mine/script')
    context = {'user_name':request.user,"name":scripts.script_name,"scripts":scripts.script,"id":id}
    template = loader.get_template('script_page2.html')
    return HttpResponse(template.render(context,request))
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

@login_required(login_url='/accounts/login/')
def profileac(request):
    'アカウントのプロフィール'
    configs = get_conf(request)
    return render(request, 'profileac.html',{'user_name':request.user,'config_name':configs.server_name,'ip':configs.server_ip,'rcon_port':configs.rcon_port,'query_port':configs.query_port,'passw':configs.passw})
spaces = 36
test_list = ""
def list_print(list_type,data):
    global test_list
    space = 12 - len(list_type)
    list_type = list_type + '　' * space
    test_list = test_list + list_type + data + "%kai"
@login_required(login_url='/accounts/login/')
def console(request):
    global test_list
    configs = get_conf(request)

    return_text = ""
    text = ""
    if request.method == "POST":
        text = request.POST.get('command')
    if not text:
        pass
    else:
        chat_flag = False #チャットであるかのフラグ
        query_flag = False #クエリであるかのフラグ
        config_flag = False #クエリであるかのフラグ
        kai_flag = False #改行を行う表であるかのフラグ
        mark_flag = False
        script_falg = False
        list_flag = False
        test_list = ""
        if text == "/markup":
            mark_flag = True
            kai_flag = True
        if text == "/query":
            query_flag = True
            kai_flag = True
        elif not text[0] == "/":
            func_du = ["say"]
            func_du.append(text)
            return_text = "/say "+text
            chat_flag = True
        elif text == "/config":
            config_flag = True
            kai_flag = True
        elif text == "/help":
            kai_flag = True
            chat_flag = True
        elif text[0:7] == "/script":
            script_falg = True
            try:
                ids = int((text.split(" "))[1])
            except ValueError:
                script_falg = False
                list_flag = True
        funcs_list = text.split("/")
        for i in range(len(funcs_list)-1):
            func_du = funcs_list[int(i)+1].split(" ")
        
        try:
            with Client(configs.server_ip, int(configs.rcon_port), passwd=configs.passw) as client:
                if chat_flag:
                    client.run(*func_du)

                elif query_flag:
                    full_stats , seed = query_full(request)
                    test_list = test_list + 'Server Full Stats@%s' % datetime.datetime.now() + "%kai%kai"
                    list_print('element','data')
                    test_list = test_list + '-'* spaces + "%kai"
                    list_print('type',str(full_stats.type))
                    list_print('session_id',str(full_stats.session_id))
                    list_print('motd',str(full_stats.host_name))
                    list_print('game_type',str(full_stats.game_type))
                    list_print('game_id',str(full_stats.game_id))
                    list_print('version',str(full_stats.version))
                    list_print('plugins',str(full_stats.plugins))
                    list_print('map',str(full_stats.map))
                    list_print('players',str(full_stats.num_players)+'/'+str(full_stats.max_players)+' '+str(full_stats.players))
                    list_print('host',str(full_stats.host_ip)+'@'+str(full_stats.host_port))
                    list_print('seed',str(seed))
                    return_text = test_list
                elif config_flag:
                    test_list = test_list + 'My config get@%s' % datetime.datetime.now() + "%kai%kai"
                    list_print('element','data')
                    test_list = test_list + '-'* spaces + "%kai"
                    list_print('name',str(configs.server_name))
                    list_print('host',str(configs.server_ip))
                    list_print('rcon',str(configs.server_ip)+"@"+str(configs.rcon_port))
                    list_print('query',str(configs.server_ip)+"@"+str(configs.query_port))
                    return_text = test_list
                elif mark_flag:
                    list_print('element','data')
                    test_list = test_list + '-'* spaces + "%kai"
                    list_print('§0',"<span style='color:#000000;'>text</span>")
                    list_print('§1',"<span style='color:#0000AA;'>text</span>")
                    list_print('§2',"<span style='color:#00AA00;'>text</span>")
                    list_print('§3',"<span style='color:#00AAAA;'>text</span>")
                    list_print('§4',"<span style='color:#AA0000;'>text</span>")
                    list_print('§5',"<span style='color:#AA00AA;'>text</span>")
                    list_print('§6',"<span style='color:#FFAA00;'>text</span>")
                    list_print('§7',"<span style='color:#AAAAAA;'>text</span>")
                    list_print('§8',"<span style='color:#555555;'>text</span>")
                    list_print('§9',"<span style='color:#5555FF;'>text</span>")
                    list_print('§a',"<span style='color:#55FFFF;'>text</span>")
                    list_print('§b',"<span style='color:#FFAA00;'>text</span>")
                    list_print('§c',"<span style='color:#FF5555;'>text</span>")
                    list_print('§d',"<span style='color:#FF55FF;'>text</span>")
                    list_print('§e',"<span style='color:#FFFF55;'>text</span>")
                    list_print('§f',"<span style='color:#FFFFFF;'>text</span>")
                    return_text = test_list
                elif script_falg:
                    configs = get_conf(request)
                    scripts = Script.objects.get(id=ids)
                    funcs = scripts.script
                    funcs_list = funcs.split("/")
                    re ="/ "
                    text2 = ""
                    for i in range(len(funcs_list)-1):
                        func_du = funcs_list[int(i)+1].split(" ")
                        text = scripts.script_name
                        try:
                            re = re+client.run(*func_du)
                        except ConnectionRefusedError as e:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'ServerNotFoundError / '
                        except ConnectionResetError as e:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'ServerNotFoundError / '
                        except NoPlayerFound as e:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'NoPlayerFoundError / '
                        except UnboundLocalError:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'SyntaxError / '
                        except UnknownCommand:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'Unknown or incomplete command / '
                        except InvalidArgument:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'InvalidArgument / '
                        except LocationNotFound:
                            text2 = logtext(request,text,"失敗")
                            re = re + 'Location could not be found. / '
                        else:
                            re = re+" / "
                        text2 = logtext(request,text,"失敗")
                    return_text = re
                elif list_flag:
                    scripts = Script.objects.all()
                    for i in scripts:
                        return_text = return_text + i.script_name+":"+str(i.id)+"%kai"
                    kai_flag = True
                else:
                    return_text = client.run(*func_du)
                text2 = logtext(request,text,"成功")
        except ConnectionRefusedError as e:
            text2 = logtext(request,text,"失敗")
            return_text = 'ServerNotFoundError'
        except ConnectionResetError as e:
            text2 = logtext(request,text,"失敗")
            return_text = 'ServerNotFoundError'
        except NoPlayerFound as e:
            text2 = logtext(request,text,"失敗")
            return_text = 'NoPlayerFoundError'
        except UnboundLocalError:
            text2 = logtext(request,text,"失敗")
            return_text = 'SyntaxError'
        except UnknownCommand:
            text2 = logtext(request,text,"失敗")
            return_text = 'Unknown or incomplete command'
        except InvalidArgument:
            text2 = logtext(request,text,"失敗")
            return_text = 'InvalidArgument'
        except LocationNotFound:
            text2 = logtext(request,text,"失敗")
            return_text = 'Location could not be found.'
        logging(text2)
        command = Command_log(command_text=text,return_text=return_text,user=request.user,time=datetime.datetime.now(),q_flag=kai_flag,chat_flag=chat_flag)
        command.save()
    latest_question_list = Command_log.objects.all()
    template = loader.get_template('console2.html')
    test = list()
    #適合するユーザーの履歴を取得
    for i in range(len(latest_question_list)):
        if latest_question_list[i].user == request.user:
            test.append(latest_question_list[i])
    test.reverse()
    #日付表記の変更
    for i in latest_question_list:
        i.time = str(i.time).replace("年","/")
        i.time = str(i.time).replace("月","/")
        i.time = str(i.time).replace("日","")
        i.time = str(i.time).replace("+"," ")
        i.time = str(i.time).replace("00:00","")
    #装飾文字のデコード
    for i in latest_question_list:
        if i.chat_flag:
            #print(i.return_text)
            #print("return")
            #i.return_text = i.return_text[0]
            #print(i.return_text)
            num = i.return_text.count("§")
            i.return_text = i.return_text.replace("§0","<br><span style='color:#000000;'>")
            i.return_text = i.return_text.replace("§1","<br><span style='color:#0000AA;'>")
            i.return_text = i.return_text.replace("§2","<br><span style='color:#00AA00;'>")
            i.return_text = i.return_text.replace("§3","<br><span style='color:#00AAAA;'>")
            i.return_text = i.return_text.replace("§4","<br><span style='color:#AA0000;'>")
            i.return_text = i.return_text.replace("§5","<br><span style='color:#AA00AA;'>")
            i.return_text = i.return_text.replace("§6","<br><span style='color:#FFAA00;'>")
            i.return_text = i.return_text.replace("§7","<br><span style='color:#AAAAAA;'>")
            i.return_text = i.return_text.replace("§8","<br><span style='color:#555555;'>")
            i.return_text = i.return_text.replace("§9","<br><span style='color:#5555FF;'>")
            i.return_text = i.return_text.replace("§a","<br><span style='color:#55FF55;'>")
            i.return_text = i.return_text.replace("§b","<br><span style='color:#55FFFF;'>")
            i.return_text = i.return_text.replace("§c","<br><span style='color:#FF5555;'>")
            i.return_text = i.return_text.replace("§d","<br><span style='color:#FF55FF;'>")
            i.return_text = i.return_text.replace("§e","<br><span style='color:#FFFF55;'>")
            i.return_text = i.return_text.replace("§f","<br><span style='color:#FFFFFF;'>")
            
            for i2 in range(num):
                i.return_text = i.return_text + "</span>"
            #print(i.return_text)

    #%kaiでの改行処理
    for i in latest_question_list:
        if i.q_flag:
            text = i.return_text 
            i.return_text = text.split("%kai")
    context = {
        'latest_question_list': test[0:5],"user_name":request.user,"debug":"","logined":request.user.is_authenticated
    }
    return HttpResponse(template.render(context, request))
def query_full(req):
    "Queryを飛ばすだけの関数。"
    configs = get_conf(req)
    with Client_q(configs.server_ip, int(configs.query_port)) as client:
        full_stats= client.stats(full=True)
    with Client(configs.server_ip, int(configs.rcon_port), passwd='minecraft') as client:
        seed = client.seed
    return full_stats, seed
@login_required(login_url='/accounts/login/')
def config_page(request):
    configs = get_conf(request)
    name = ""
    try:
        name_c = configs.server_name
    except:
        name_c = ""
    try:
        ip_c = configs.server_ip
    except:
        ip_c = ""
    try:
        qport_c = configs.query_port
    except:
        qport_c = ""
    try:
        rport_c = configs.rcon_port
    except:
        rport_c = ""
    try:
        passw_c = configs.passw
    except:
        passw_c = ""
    if request.method == "POST":
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        qport = request.POST.get('qport')
        rport = request.POST.get('rport')
        passw = request.POST.get('passw')
        if not name and not ip and not qport and not rport and not passw:
            pass
        else:
            configs_list = Config.objects.all()
            for configs in configs_list:
                if configs.user == request.user:
                    break
            if configs == None:
                pass
            else:
                configs.delete()
            config_data = Config(server_name=name,user=request.user,server_ip=ip,rcon_port=rport,query_port=qport,passw=passw)
            config_data.save()
        return redirect("/mine/profile/")
    context = {'user_name':request.user,'name':name_c,"ip":ip_c,"qport":qport_c,"rport":rport_c,"passw":passw_c}
    template = loader.get_template('config_page.html')
    return HttpResponse(template.render(context,request))
@login_required(login_url='/accounts/login/')
def code_page(request):
    codes = Code.objects.all()
    code = codes[0]
    name_c = ""
    code_c = ""
    inter_c = ""

    name_c = code.name
    code_c = code.code
    inter_c = code.code_interval
    if request.method == "POST":
        name = request.POST.get('name')
        script = request.POST.get('code')
        inter = request.POST.get('inter')
        if not name and not script and not inter:
            pass
        else:
            code.delete()
            code_new = Code(name=name,code=script,code_interval=inter)
            code_new.save()
    context = {'user_name':request.user,'name':name_c,"code":code_c,"inter":inter_c}
    template = loader.get_template('code_page.html')
    return HttpResponse(template.render(context,request))

def help(request):
    context = {'user_name':request.user}
    template = loader.get_template('helppage.html')
    return HttpResponse(template.render(context,request))

def kaigoyu(request):
    context = {'kaigyou':["test1","test2","test3","test4"]}
    template = loader.get_template('kaigyou.html')
    return HttpResponse(template.render(context,request))

def index(request):
    context = {
        "user_name":request.user,"logined":request.user.is_authenticated
    }
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))

def test(request):
    context = {
        "debug":"<span style='color:red;'>まっかっか？</span>"
    }
    template = loader.get_template('testpage.html')
    return HttpResponse(template.render(context,request))

def debug(request):
    context = {
        "debug":User.objects.all()
    }
    template = loader.get_template('debug.html')
    return HttpResponse(template.render(context,request))
#フラグ類
end_flag = False
exit_flag = False
def loop_code():
    global exit_flag, end_flag
    print("[Server]Thread started.")
    while True:
        codes = Code.objects.all()
        for code in codes:
            text = code.code
            text = text.replace("/","")
            text = text.split(" ")
            #print(code.code_interval)
            if int(code.code_interval) <= 0:
                #print("[Code]if")
                pass
            else:
                with Client("127.0.0.1", 25575, passwd="minecraft") as client:
                    print("[Code]"+client.run(*text))
                time.sleep(int(code.code_interval))

def tasks():
    backbround = threading.Thread(target=loop_code)
    backbround.start()

tasks()