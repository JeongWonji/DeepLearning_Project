from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping
from parkingLot.models import Parking
from django.http import JsonResponse
from datetime import datetime

@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self, request):
        return render(request, 'index.html')

    @request_mapping("/check", method="get")
    def check_parking(self, request):
        try:
            obj = Parking.objects.filter(state="0").order_by('-id') #최신 순서로 나오게끔
            context = {'obj': obj}
            return render(request, 'check-parking.html', context)
        except:
            print("db가져오기 실패")


    @request_mapping("/enter", method="get")
    def enter(self, request):
        try:
            obj = Parking.objects.all().order_by('-id') #최신 순서로 나오게끔
            context = {'obj': obj}
            return render(request, 'car-enter.html', context)
        except:
            print("db가져오기 실패")

    @request_mapping("/dashboard", method="get")
    def dashboard(self, request):
        return render(request, 'dashboard.html')

    @request_mapping("/dataset", method="get")
    def dataset(self, request):
        img = request.GET.get('img')
        number = request.GET.get('number')
        handicap = request.GET.get('handicap')
        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            Parking.objects.create(img=img, car_number=number, handicap=handicap, enter=date).save()
            print("db 저장 성공")
        except:
            print("db 저장 실패")

        return JsonResponse({"result": 1})

    @request_mapping("/numbercompare", method="get")
    def numbercompare(self, request):
        number = request.GET.get('number')
        try:
            obj = Parking.objects.get(car_number=number)
            if obj.car_number == number:
                if obj.handicap == "0": #장애인 차량이 아닌경우
                    obj.state = "0"
                    obj.save()
                    return JsonResponse({"result": 0})
                elif obj.handicap == "1": #장애인 차량인 경우
                    obj.state = "1"
                    obj.save()
                    return JsonResponse({"result": 1})
            else:
                print("맞는 번호판이 없음")
        except:
            print("자동차 번호 불러오기 실패")

        return JsonResponse({"result": -1})

    @request_mapping("/cardelete/<int:pk>", method="get")
    def cardelete(self, request, pk):
        try:
            Parking.objects.get(id=pk).delete()
            return JsonResponse({"result": 1})
        except:
            return JsonResponse({"result": 0})

    @request_mapping("/image/<int:pk>", method="get")
    def image(self, request, pk):
        try:
            obj = Parking.objects.get(id=pk)
            return render(request, 'image.html', {'context': obj})
        except:
            print("불러오기 실패")

    @request_mapping("/updateNumber/<int:pk>", method="get")
    def updateNumber(self, request, pk):
        number = request.GET.get('carnumber')
        try:
            obj = Parking.objects.get(id=pk)
            obj.car_number = number
            obj.save()
            return redirect("/enter")
        except:
            print("db 불러오기 실패")

    @request_mapping("/handicapUpdate/<int:pk>", method="get")
    def handicapUpdate(self, request, pk):
        try:
            obj = Parking.objects.get(id=pk)
            obj.handicap = "1"
            obj.state = "1"
            obj.save()
            return redirect("/check")
        except:
            print("db 불러오기 실패")