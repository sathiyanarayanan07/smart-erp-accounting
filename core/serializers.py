from rest_framework import serializers
from . models import role1,product_details,QA,product,accountent,Admin,product_details,product_material,product_options,plan_product,schedule,account_page


class role1Serializer(serializers.ModelSerializer):
    class Meta:
        model = role1
        fields = "__all__"

class product_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_details
        fields = "__all__"

class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields ="__all__"

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields ="__all__"

class accountentSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountent
        fields ="__all__"

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields ="__all__"

class product_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_details
        fields ="__all__"

class product_materialSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_material
        fields = "__all__"

class product_optionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_options
        fields ="__all__"

class plan_productSerializer(serializers.ModelSerializer):
    class Meta:
        model = plan_product
        fields ="__all__"

class scheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = schedule
        fields ="__all__"


class account_pageSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_page
        fields ="__all__"
