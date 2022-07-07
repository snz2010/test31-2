from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated # 30-06 ...
from ads.serializers import AdSerializer, AdDetailSerializer, SelectionListSerializer, SelectionDetailSerializer, SelectionSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views import View

from django.db.models import Count, Avg, Q, F
from django.conf import settings
from django.core.paginator import Paginator
from ads.models import Category, Ad
from ads.permissions import AdUpdatePermission, SelectionUpdatePermission # 30-06 ...
import json
import pandas as pandas
from users.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView


# стартовая страница
class IndexView(View):
    def get(self, request, *args, **kwargs):
        responce = {"status": "ok"}
        return JsonResponse(responce, safe=False, json_dumps_params={"ensure_ascii": False})


# загрузка картинки в объявление
@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ["image"] # add another fields?

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse(({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "category": self.object.category,
            "image": self.object.image.url if self.object.image else None,
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# просмотр всех объявлений + поиск по тексту из названия
class AdView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    def get(self, request, *args, **kwargs):
        # поиск по тексту объявления -----------------------
        search_txt = request.GET.get('text', None)
        if search_txt:
            self.queryset = self.queryset.filter(
                name__icontains=search_txt # почему icontains работает как contains?
            )
        # поиск по диапазону цен ---------------------------
        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        price_query = None
        if price_from:
            price_query = Q(price__gte=price_from)
        if price_from and price_to:
            price_query |= Q(price__lte=price_to)
        if price_to:
            price_query = Q(price__lte=price_to)
        if price_query:
            self.queryset = self.queryset.filter(price_query)
        # поиск по категории -------------------------------
        cat_txt = request.GET.get('cat', None)
        if cat_txt:
            self.queryset = self.queryset.filter(category=cat_txt)
        # поиск по локации ---------------------------------
        loc_txt = request.GET.get('location', None)
        if loc_txt:
            self.queryset = self.queryset.filter(author__locations__name__icontains=loc_txt)

        return super().get(request, *args, **kwargs)

# детальный просмотр объявления
class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    # 30-06 ...
    permission_classes = [IsAuthenticated] #, AdUpdatePermission]



# создание объявления
@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = get_object_or_404(User, id__iexact=ad_data["author_id"])
        category = get_object_or_404(Category, id__iexact=ad_data["category_id"])

        ad = Ad.objects.create(
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            image=ad_data["image"],
            category=category
        )

        return JsonResponse(({
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category.name,
            "image": ad.image.url if ad.image else None,
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# редактирование объявления
@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, id__iexact=ad_data["author_id"])
        category = get_object_or_404(Category, id__iexact=ad_data["category_id"])

        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.author = author
        self.object.category = category
        self.object.is_published = ad_data["is_published"]

        self.object.save()

        return JsonResponse(({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
        }), safe=False, json_dumps_params={"ensure_ascii": False})


# удаление объявления
''' 30-06 ...
@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({
            "Удаление из Ad": "успешно",
        }, json_dumps_params={"ensure_ascii": False}, status=200)
...30-06 '''
class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdUpdatePermission]




# просмотр категорий
class CategoryView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")
        responce = []
        for cat in self.object_list:
            responce.append({
                "id": cat.id,
                "name": cat.name,
            })
        return JsonResponse(responce, safe=False, json_dumps_params={"ensure_ascii": False})


# детальный просмотр категории
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, safe=False, json_dumps_params={"ensure_ascii": False})


# создание категории
@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        cat = Category.objects.create(
            name=cat_data["name"],
        )
        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, safe=False, json_dumps_params={"ensure_ascii": False})


# обновление категории
@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)
        self.object.name = cat_data["name"]
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        }, safe=False, json_dumps_params={"ensure_ascii": False})


# удаление категории
@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({
            "Удаление из Cat": "успешно",
        }, json_dumps_params={"ensure_ascii": False}, status=200)


################################################################################
# заполнение таблицы категорий, используя данные из файла
class AddToCat(View):
    def get(self, request):
        csv_data = pandas.read_csv('ads/data/categories.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            Category.objects.create(
                name=csv_data["name"][i],
            )
            i += 1
        return JsonResponse("Add to table Cat - Ok", safe=False, status=200)


################################################################################
# заполнение таблицы объявлений, используя данные из файла
class AddToAd(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def get(self, request):
        csv_data = pandas.read_csv('ads/data/ads.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            author = get_object_or_404(User, id=csv_data["author_id"][i])
            category = get_object_or_404(Category, id=csv_data["category_id"][i])

            ad = Ad.objects.create(
                name=csv_data["name"][i],
                author=author, # почему не работает ????
                category=category, # почему не работает ????
                price=csv_data["price"][i],
                description=csv_data["description"][i],
                is_published=csv_data["is_published"][i],
                image=csv_data["image"][i]
            )
            i += 1
        return JsonResponse("Add to table Ad - Ok", safe=False, status=200)


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer

class SelectionRetrieveView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer

class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]

class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated,SelectionUpdatePermission]

class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated,SelectionUpdatePermission]

