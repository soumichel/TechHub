from django.template import loader
from django.http import HttpResponse

def techhub(request):
    template = loader.get_template('techhub.html')
    context = {
        "nome_empresa": "TechHub",
        "slogan": "O lugar perfeito para encontrar seus periféricos!",
        "contato": {
            "email": "contato@techub.com",
            "telefone": "(00) 00000-0000"
        },
        "usuarioativo": True
    }
    return HttpResponse(template.render(context, request))
