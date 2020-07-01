from rest_framework import status, generics, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView

# Create your views here.
from api.models import Book
from utils.response import APIResponse
from .serializers import BookModelSerializer


class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_list, many=True).data

        return APIResponse(results=data_ser)

# GenericAPIView继承了APIView, 两者完全兼容
# 重点分析GenericAPIView 在APIView的基础上完成了哪些事情
class BookGenericAPIView(GenericAPIView,
                         ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,):
    # 获取当前视图所操作的模型 与序列化器类
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer  #指定使用的序列化器
    # 指定(重写，默认是pk)获取单条信息的主键的名称
    lookup_field = "id"

    # 通过继承ListModelMixin 提供self.list完成了查询所有
    # 通过继承RetrieveModelMixin 提供了self.retrieve 完成了查询单个
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    # 查询所有:GenericAPIView和ListModelMixin的配合使用
    # def get(self, request, *args, **kwargs):
    #     # GenericAPIView和ListModelMixin的list方法结合实现查询所有
    #     return self.list(request, *args, **kwargs)

    # 查询单个
    # def get(self, request, *args, **kwargs):
    #     book_list = self.get_object()  #通过url的参数,获取单个对象
    #     data_ser = self.get_serializer(book_list).data#序列化
    #
    #     return APIResponse(results=data_ser)

    # 查询所有
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    #
    # def list(self, request, *args, **kwargs):
    #     # 获取book模型的所有的数据
    #     book_list = self.get_queryset()
    #     # 获取要使用序列化器
    #     data_ser = self.get_serializer(book_list, many=True)
    #     data = data_ser.data
    #
    #     return APIResponse(results=data)

    # 新增图书  通过继承CreateModelMixin 来获得self.create方法  内部完成了新增
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 单整体改 继承UpdateModelMixin，含有updata方法,默认修改整体
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 单局部改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # # 通过继承DestroyModelMixin 获取self
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(http_status=status.HTTP_200_OK)


class BookListAPIVIew(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

class BookGenericViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    # 如何确定post请求是需要登录
    def user_login(self, request, *args, **kwargs):
        # 可以在此方法中完成用户登录的逻辑
        return self.retrieve(request, *args, **kwargs)

    def get_user_count(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)




