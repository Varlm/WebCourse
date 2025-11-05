from django.shortcuts import render
from django.http import HttpResponse
from museum.models import Artifact
from django.views.generic import TemplateView
# Create your views here.
class showArtifactsView(TemplateView):
    template_name="artifacts/show_artifacts.html"
    def get_context_data(self,**kwargs:any)->dict[str, any]:
        context=super().get_context_data(**kwargs)
        context['artifacts']=Artifact.objects.all()
        return context
