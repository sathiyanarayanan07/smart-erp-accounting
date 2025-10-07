from rest_framework import serializers
from .models import customers,vendor,Account,Journal,JournalEntry,JournalItems,customer_contact,product,InvoiceLine,salesInvoice,vendor_product,purchaseinvoice
from .models import InvoiceStatus,purchaseInvoiceLine,purchaseInvoiceStatus,customer_payment,vendor_payment




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields ="__all__"


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal    
        fields ="__all__"   


class JournalItemsSerializer(serializers.ModelSerializer):
    journalentry = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = JournalItems
        fields =["account","journalentry","partner","label","debit","credit"]


class journalentrySerializer(serializers.ModelSerializer):
    items = JournalItemsSerializer(many=True)
    
    class Meta:
        model = JournalEntry
        fields = ["journal", "accounting_date", "description", "reference","items","status"]

    def create(self ,validated_data):
        item_data = validated_data.pop("items")
    

        journalentrys= JournalEntry.objects.create(**validated_data)


        for item in item_data:
            JournalItems.objects.create(journalentry=journalentrys,**item)




        if JournalItems.total_debits() != JournalItems.total.credits():
            raise serializers.ValidationError("Journal Entry is no balanced (debit ≠ credit)")

        return journalentrys    





class customersSerializer(serializers.ModelSerializer):
    class Meta:
        model = customers
        fields ="__all__"

class customer_contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer_contact
        fields ="__all__"

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model =product
        fields ="__all__"
        


class InvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLine  
        fields ="__all__" 
        extra_kwargs = {
            "invoices": {"read_only":True}
        } 

class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True)
    class Meta:
        model = salesInvoice
        fields = ["customer","invoice_Date","Due_Date","payments_terms","journals","lines","Status"]      

    def create(self,validated_data):
        inv_lines_data =validated_data.pop('lines')

        invoice_instance = salesInvoice.objects.create(**validated_data)

        for line in inv_lines_data:
            InvoiceLine.objects.create(invoices=invoice_instance,**line)
            invoice_instance.calculate_total()

        if invoice_instance.Status == InvoiceStatus.DRAFT:
            invoice_instance.post()
          

        return invoice_instance    




class customer_paymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer_payment
        fields =['customer','invoice','payment_date','amount','journal','reference','status']

    def create(self, validated_data):
        payment =customer_payment.objects.create(**validated_data)
        payment.post()
        return payment    


class vendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = vendor
        fields ="__all__"   

class vendor_productSerializer(serializers.ModelSerializer):
    class Meta:
        model =vendor_product
        fields ="__all__"



class purchaseInvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaseInvoiceLine
        fields ="__all__"
        extra_kwargs = {
            "invoices": {"read_only":True}
        } 


class purchaseinvoiceSerializer(serializers.ModelSerializer):
    lines=purchaseInvoiceLineSerializer(many=True)
    class Meta:
        model =purchaseinvoice
        fields=["vendor","invoice_Date","Due_Date","payments_terms","Status","journals","lines"]

    def create(self, validated_data):
        lines= validated_data.pop('lines')

        purchaseinvoice_instance =purchaseinvoice.objects.create(**validated_data)    

        for line in lines:
            purchaseInvoiceLine.objects.create(invoices=purchaseinvoice_instance,**line)
            purchaseinvoice_instance.calculate_total_vendor()

        if purchaseinvoice_instance.Status == purchaseInvoiceStatus.DRAFT:
            purchaseinvoice_instance.post()

            return purchaseinvoice_instance


class vendor_paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendor_payment
        fields =["vendors","invoice","payment_date","amount","journal","reference","status"]

    def create(self, validated_data):
        vendorpayment=vendor_payment.objects.create(**validated_data)
        vendor_payment.post()
        return vendor_payment    