#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializers.py
@说明    :序列化
@时间    :2023/04/22 17:26:05
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
   
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from bayke.conf import bayke_settings
from bayke.models.user import BaykeUser, BaykeVerifyCode


class BaykeUserSerializer(serializers.ModelSerializer):
    """ 一对一关联用户信息 """
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeUser
        exclude = ("add_date", "pub_date")
        

class UserSerializer(serializers.ModelSerializer):
    """ 用户 """
    username = serializers.ReadOnlyField()
    baykeuser = BaykeUserSerializer(many=False, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'baykeuser')
        

class ObtainEmailCodeSerializer(serializers.ModelSerializer):
    """ 邮箱发送验证码 """
    
    email = serializers.EmailField(
        label="邮箱", 
        max_length=150, 
        min_length=3
    )
    code = serializers.ReadOnlyField()

    class Meta:
        model = BaykeVerifyCode
        fields = ('email', 'code')

    def create(self, validated_data):
        data = validated_data
        from django.utils import timezone
        from bayke.utils import code_random

        code = BaykeVerifyCode.objects.filter(email=data['email']).first()

        if code:
            # nd = timezone.now() - datetime.timedelta(seconds=60)
            nd = timezone.now() - bayke_settings.EMAIL_CODE_EXP
            # 判断是否过期，刷新验证码
            if nd > code.pub_date:
                code.code = code_random()
                code.save()
            else:
                # 这里只发送邮件
                code.save_send_main(code.code)
        else:
            code = BaykeVerifyCode.objects.create(email=data['email'])     
        return code


class CheckEmailCodeSerializer(serializers.Serializer):
    
    """ 验证码效验 """
    
    code = serializers.CharField(
        label="验证码", 
        max_length=bayke_settings.CODE_LENGTH, 
        min_length=bayke_settings.CODE_LENGTH
    )
    email = serializers.EmailField(label="邮箱", max_length=150)
    
    def validate(self, attrs):
        email_codes = BaykeVerifyCode.objects.filter(email=attrs['email'], code=attrs['code'])
        if not email_codes.exists():
            raise serializers.ValidationError("该验证码不存在！")
        else:
            code = email_codes.first()
            from django.utils import timezone
            nd = timezone.now() - bayke_settings.EMAIL_CODE_EXP
            # 判断是否过期，刷新验证码
            if nd > code.pub_date:
                raise serializers.ValidationError("该验证码已过期，请重新获取！")
        return attrs
    
    
class RegisterSerializer(CheckEmailCodeSerializer):
    
    """ 用户注册 """
    
    username = serializers.CharField(label="用户名", max_length=32, min_length=2, validators=[
        UniqueValidator(queryset=get_user_model().objects.all(), message="该用户名已存在，请更换！")
    ])
    password = serializers.CharField(label="密码", max_length=36, min_length=8, write_only=True)
    email = serializers.EmailField(label="邮箱", max_length=100, validators=[
        UniqueValidator(queryset=get_user_model().objects.all(), message="该邮箱已存在，请更换！")
    ])
    code = serializers.CharField(
        label="验证码", 
        max_length=bayke_settings.CODE_LENGTH, 
        min_length=bayke_settings.CODE_LENGTH,
        write_only=True
    )
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
    def validate(self, attrs):
        # 如果不需要邮箱验证只需要注释掉下边这句
        super().validate(attrs)  # 邮箱验证 
        del attrs["code"]
        return attrs


class BaykeProductBannerSerializer(serializers.ModelSerializer):
    """ 商品序列化 """
    
    class Meta:
        from bayke.models.product import BaykeProductBanner
        model = BaykeProductBanner
        fields = ("id", "img")


class BaykeProductSpecOptionSerializer(serializers.ModelSerializer):
    """ 商品spec option """
    
    # spec = serializers.StringRelatedField()
    
    class Meta:
        from bayke.models.product import BaykeProductSpecOption
        model = BaykeProductSpecOption
        fields = ('id', 'name', 'spec')


class BaykeProductSPecSerializer(serializers.ModelSerializer):
    """ 商品spec """
    
    class Meta:
        from bayke.models.product import BaykeProductSpec
        model = BaykeProductSpec
        fields = "__all__"


class BaykeProductSKUSerializer(serializers.ModelSerializer):
    """ 商品sku """
    
    options = BaykeProductSpecOptionSerializer(many=True)
    
    class Meta:
        from bayke.models.product import BaykeProductSKU
        model = BaykeProductSKU
        fields = "__all__"


class BaykeProductCategorySerializer(serializers.ModelSerializer):
    """ 商品分类 """
    
    # parent = serializers.StringRelatedField()
    
    class Meta:
        from bayke.models.product import BaykeProductCategory
        model = BaykeProductCategory
        exclude = ("site", "desc", "keywords", "is_del")
    

class BaykeProductSPUSerializer(serializers.ModelSerializer):
    """ 商品序列化 """
    
    cates = BaykeProductCategorySerializer(many=True, read_only=True)
    baykeproductbanner_set = BaykeProductBannerSerializer(many=True, read_only=True)
    baykeproductsku_set = BaykeProductSKUSerializer(many=True, read_only=True)
    specs = serializers.SerializerMethodField()
    
    class Meta:
        from bayke.models.product import BaykeProductSPU
        model = BaykeProductSPU
        fields = "__all__"
        
    def get_specs(self, obj):
        """ 整理specs规格列表 """
        specs = obj.baykeproductsku_set.values("options__spec__name", "options__name")
        specs_items = {}
        for spec in specs:
            if spec["options__spec__name"] not in specs_items:
                specs_items[spec["options__spec__name"]] = []
            for k in specs_items.keys():
                if k == spec["options__spec__name"]:
                    specs_items[spec["options__spec__name"]].append(spec["options__name"])
        return specs_items


###################################################################
# cart start 购物车序列化

class BaykeCartSPUSerializer(BaykeProductSPUSerializer):
    pass
class BaykeCartSKUSerializer(BaykeProductSKUSerializer):
    spu = BaykeCartSPUSerializer(many=False, read_only=True)
class BaykeCartSerializer(serializers.ModelSerializer):
    """ 购物车序列化类 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sku = BaykeCartSKUSerializer(many=False, read_only=True)
    
    class Meta:
        from bayke.models.cart import BaykeCart
        model = BaykeCart
        # fields = "__all__"
        exclude = ("site", "is_del")
    
    def create(self, validated_data):
        from django.db.utils import IntegrityError
        try:
            instance = super().create(validated_data)
            return instance   
        except IntegrityError:
            from django.db.models import F
            from bayke.models.cart import BaykeCart
            carts = BaykeCart.objects.filter(
                owner=self.context['request'].user, 
                sku=validated_data['sku']
            )
            carts.update(count=F("count")+validated_data["count"])
            return carts.first()
    
    
class BaykeCartUpdateCountSerializer(serializers.ModelSerializer):
    """ 购物车数量修改序列化 """ 
    class Meta:
        from bayke.models.cart import BaykeCart
        model = BaykeCart
        fields = ("id", "count")

# cart end 购物车序列化
###################################################################
###################################################################
# order start 订单序列化

class BaykeOrderSerializer(serializers.ModelSerializer):
    """ 订单序列化基类 """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        from bayke.models.order import BaykeOrder
        model = BaykeOrder
        exclude = ("site", "is_del")
        

class BaykeOrderSKUSerializer(serializers.ModelSerializer):
    """ 这个接口轻易不用， 后期可能会调整，慎用
    """
    order = BaykeOrderSerializer(many=False)
    is_commented = serializers.ReadOnlyField()
    
    class Meta:
        from bayke.models.order import BaykeOrderSKU
        model = BaykeOrderSKU
        exclude = ("site", "is_del")
        
    def create(self, validated_data):
        # 该create方法慎用
        order = validated_data.pop("order")
        from bayke.models.order import BaykeOrder
        order = BaykeOrder.objects.create(**order)
        validated_data['options'] = list(validated_data['sku'].options.values("spec__name", "name"))
        validated_data['title'] = validated_data['sku'].spu.title
        validated_data['content'] = validated_data['sku'].spu.content
        validated_data['price'] = validated_data['sku'].price
        validated_data['order'] = order
        return super().create(validated_data)
        

class BaykeOrderCreateSerializer(BaykeOrderSerializer):
    """ 创建订单序列化 """
    
    baykeordersku_set = BaykeOrderSKUSerializer(many=True, read_only=True)

    def create(self, validated_data):
        """前端需要传递的数据结构
        {
            "baykeordersku_set": [
                {   
                    "sku": 2,   # 商品规格sku id => BaykeProductSKU
                    "count": 2  # 购买数量
                }
            ],
            "total_amount": 15, # 任意数字，总价由后台负责计算【可选】
            "order_mark": "",   # 订单备注
            "name": "张真",
            "phone": "18391037602",
            "email": "asda@qq.com",
            "address": "陕西咸阳"
        }
        """
        baykeordersku_set = self.context['request'].data.pop("baykeordersku_set")
        order = super().create(validated_data)
        self.create_order_sku(baykeordersku_set, order)
        return order

    def create_order_sku(self, skus:list, order):
        """ 保存关联订单商品 """
        from bayke.models.product import BaykeProductSKU
        from bayke.models.order import BaykeOrderSKU
        for sku in skus:
            sku['order'] = order
            try:
                sku_obj = BaykeProductSKU.objects.get(id=int(sku.get('sku')))
                sku["title"] = sku_obj.spu.title
                sku["price"] = sku_obj.price
                sku["content"] = sku_obj.spu.content
                sku["options"] = list(sku_obj.options.values("spec__name", "name"))
                sku.pop('sku')
                BaykeOrderSKU.objects.create(sku=sku_obj, **sku)
            except BaykeProductSKU.DoesNotExist:
                raise serializers.ValidationError("传递的sku参数有误")
    
# order end 订单序列化
###################################################################
