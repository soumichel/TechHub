from django.template import loader
from django.http import HttpResponse

def teste(request):
    template = loader.get_template('paginateste.html')
    return HttpResponse(template.render())

def testeparametros(request):
    template = loader.get_template('testeparametros.html')
    context = {
        "nome": "José Silva",
        "idade": 30,
        "email": "jose.silva@email.com",
        "telefone": "3333-1234",
        "usuarioativo": True
    }
    return HttpResponse(template.render(context, request))