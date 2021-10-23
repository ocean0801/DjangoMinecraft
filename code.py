from rconc.models import Code

codes = Code.objects.all()
for code in codes:
    print(code.name)