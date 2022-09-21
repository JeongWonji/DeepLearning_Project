from django_request_mapping import UrlPattern
from parkingLot.views import MyView

urlpatterns = UrlPattern()
urlpatterns.register(MyView)