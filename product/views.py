from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from product.models import *
from product.serializers import *
from rest_framework.response import *
from rest_framework import status
from django.db.models import Count
from product.filter import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from product.paginations import DefaultPagination
from api.permissions import *
from product.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    permission_classes=[IsAdminOrReadOnly]
    search_fields=['name','description']
    ordering_fields=['price','updated_at','size']
    @swagger_auto_schema(
            operation_summary='Retrive a list of product',
            operation_description='List of all Products GET ',
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Create Product',
            operation_description='Admin can create a new Product',       

    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='update the product'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Product show the id '
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can Edit the Product'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin Delete the Products'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ProductImageViewSet(ModelViewSet):
    serializer_class=ProductImageSerializer
    permission_classes=[IsAdminOrReadOnly]
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))
    
    @swagger_auto_schema(
            operation_summary='everyone can see the Product images'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can image update'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Product image show the id any one'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can Edit the images'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can change the product and images'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can delete the Product'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer
    @swagger_auto_schema(
            operation_summary='Retrive a list of Category'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='only Admin can Create the Category',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='To view my category by id'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Admin can edit categories.'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='Only admin can update categories.'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes=[IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'product_id':self.kwargs.get('product_pk')}
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    @swagger_auto_schema(
            operation_summary='every one can see the images'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary='User can Review any products')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary=''
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary='only User can Edit the hes reviews'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary=''
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary='only Admin can delete the reviews')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)