from rest_framework import serializers, exceptions

from api.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    """
    出版社的序列化器
    """

    class Meta:
        # 指定序列化的模型
        model = Press
        # 指定要序列化的字段
        fields = ("press_name", "address", "pic")


class BookModelSerializer(serializers.ModelSerializer):
    # 为序列化器自定以字段 (不推荐)
    # aaa = serializers.SerializerMethodField()
    #
    # def get_aaa(self, obj):
    #     return "aaa"

    # 自定义连表查询  查询图书时将图书对应的出版的信息完整的查询出来
    # 可以在序列化器中嵌套另一个序列化器来完成多表查询
    # 需要与图书表的中外键名保持一致  在连表查询较多字段时推荐使用
    publish = PressModelSerializer()

    class Meta:
        # 指定当前序列化器要序列化的模型
        model = Book
        # 指定你要序列化模型的字段
        # fields = ("book_name", "price", "pic", "publish_name", "press_address", "author_list", "publish")
        fields = ("book_name", "price", "pic", "publish")

        # 可以直接查询所有字段
        # fields = "__all__"

        # 可以指定不展示哪些字段
        # exclude = ("is_delete", "create_time", "status")

        # 指定查询深度  关联对象的查询  可以查询出有外键关系的信息
        # depth = 1


class BookDeModelSerializer(serializers.ModelSerializer):
    """
    反序列器  数据入库使用
    """

    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")

        # 添加DRF所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名太短啦~"
                }
            },
            "price": {
                "max_digits": 5,
                "decimal_places": 2,
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

# 序列化器定义了要使用
class BookListSerializer(serializers.ListSerializer):
    # 使用此序列化器完成或修改多个对象
    def update(self, instance, validated_data):
        # print(self)  #当前序列化器类
        # print(instance) #要修改的原对象
        # print(validated_data) #新的数据
        # 通过循环一个一个的进行修改
        for index, obj in enumerate(instance):
            # 每遍历一次 就修改一个对象的数据
            self.child.update(obj, validated_data[index])

        return instance

class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields应该填写哪些字段  应该填写序列化与反序列化字段的并集
        fields = ("book_name", "price", "publish", "authors", "pic")
        # 为修改多个图书对象提供ListSerializer
        list_serializer_class=BookListSerializer

        # 通过此参数指定哪些字段是参与序列化的  哪些字段是参与反序列化的
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短啦~"
                }
            },
            # 指定此字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        print(self.context.get("request"))
        return value

    # 全局校验钩子  可以通过attrs获取到前台发送的所有的参数
    def validate(self, attrs):

        price = attrs.get("price", 0)
        # 没有获取到 price  所以是 NoneType
        if price > 100:
            raise exceptions.ValidationError("书籍价格过高")

        return attrs