def logtext(req,text):
    ipadd = req.META.get('REMOTE_ADDR')
    return text+"の実行に成功しました。-%s" % 1 + " on IP" + ipadd