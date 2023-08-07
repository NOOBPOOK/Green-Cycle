from django.contrib import admin
from website.models import Feedback, MetalRequest, PaperRequest, GlassRequest, PlasticRequest, ClothesRequest, EwasteRequest

admin.site.register(Feedback)
admin.site.register(MetalRequest)
admin.site.register(PaperRequest)
admin.site.register(GlassRequest)
admin.site.register(PlasticRequest)
admin.site.register(ClothesRequest)
admin.site.register(EwasteRequest)
