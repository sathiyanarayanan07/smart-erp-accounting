from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import customers,vendor,Account,Journal,JournalEntry,JournalItems,customer_contact,product,salesInvoice,InvoiceLine,vendor_product,customer_payment,vendor_payment,purchaseinvoice
from .serializers import journalentrySerializer,JournalItemsSerializer,JournalSerializer,AccountSerializer,customersSerializer,customer_contactSerializer,productSerializer,InvoiceSerializer,InvoiceLineSerializer,vendor_productSerializer,purchaseinvoiceSerializer,vendor_paymentSerializer,customer_paymentsSerializer

# Create your views here.

# account #
@api_view(['POST'])
def account_create(request):
    name =request.data.get('name')
    account_Type =request.data.get('account_Type')
    category =request.data.get('category')
    parent_id =request.data.get('parent')
    description =request.data.get('description')

    parent_instance = None


    if parent_id:
        parent_instance =Account.objects.filter(id=parent_id).first()
        if not parent_instance:
            return Response({"parent_id is not found"},status=400)


    account_create = Account.objects.create(
        name=name,
        account_Type=account_Type,
        category =category,
        parent =parent_instance,
        description=description,

        

    )
    account_create.save()

    if not account_create:
        return Response({"msg":"account not created"},status=400)
    
    return Response({'msg':'account create successfully'},status=200)


@api_view(['GET'])
def account_list(request):
    list =Account.objects.all()
    serializer = AccountSerializer(list,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def account_details(request):
    try:
        details =Account.objects.all()

        if not details:
            return Response ({"msg":"account is not found"},status=400)
        
        account=[]
        for acc in details:
            account.append({
                'id':acc.id,
                'code':acc.code,
                'name':acc.name,
                'account_Type':acc.account_Type,
                "parent":acc.parent.id if acc.parent else None,
                'category':acc.category,
                'description':acc.description,
                "balance":acc.balance
                


            })
        return Response(account,status=200)
        
    except Exception as e:
        return Response({'msg':'account details is {str:{e}}'},status=400)


@api_view(['PUT'])
def account_update(request,id):
    account_instance = Account.objects.filter(id=id).first()
    if not account_instance:
        return Response({"msg":"account update not found"},status=400)
    
    account_instance.name = request.data.get("name", account_instance.name)
    account_instance.account_Type = request.data.get("account_Type", account_instance.account_Type)
    account_instance.category = request.data.get("category", account_instance.category)
    account_instance.description = request.data.get("description",account_instance.description)


    parent_id = request.data.get('parent')
    if parent_id is not None:
        parent_instance =Account.objects.filter(id=parent_id).first()
    if not parent_instance:
        return Response({"msg":"parent account is not found"},status=400)
    account_instance.parent = parent_instance    

    account_instance.save()

    return Response({"msg":"account updated successfully"},status=200)


@api_view(['DELETE'])
def Account_deleted(request,id):
    Account_deleted = Account.objects.filter(id=id).delete()
    if not Account_deleted:
        return Response({"msg":"Account not deleted "},status=400)
    
    return Response({"msg":"Account delete successfully"},status=200)


## journal ##

@api_view(['POST'])
def journal_create(request):
    try:
        journal_name=request.data.get('journal_name')
        type= request.data.get('type')
        description =request.data.get('description')
        
        create_journal =Journal.objects.create(
             journal_name=journal_name,
             type=type,
             description=description
              )
        
        return Response({"msg":"journal created successfullt",
                         "id":create_journal.id,
                         "code": create_journal.code,   
                         "journal_name": create_journal.journal_name,
                         "type": create_journal.type,
                         "description": create_journal.description
                         },status=201)
    except Exception as e:
        return Response({"error":str(e)},status=400)


@api_view(['GET'])
def journal_list(request):
    list =Journal.objects.all()
    serializer = JournalSerializer(list,many=True)
    return Response(serializer.data)


##journal_details ##
@api_view(['GET'])
def journal_details(request):
    try:
        details = Journal.objects.all()

        if not details:
            return Response ({"msg":"journal details is not found"},status=200)
        

        journal_list=[]
        for data in details:
            journal_list.append({
                "id":data.id,
                "code":data.code,
                "journal_name":data.journal_name,
                "type":data.type,
                "description":data.description
            
            })
        return Response(journal_list,status=200)
        
    except Exception as e:
        return Response({"msg":"journal details is {str:{e}}"},status=400)    


    
@api_view(["PUT"])
def journal_update(request,id):

    journal_instance =Journal.objects.filter(id=id).first()
    if not journal_instance:
        return Response({"msg":"journal data is not updated"},status=400)
    
    journal_instance.code =request.data.get('code',journal_instance.code)
    journal_instance.journal_name=request.data.get('journal_name',journal_instance.journal_name)
    journal_instance.type=request.data.get('type',journal_instance.type)
    journal_instance.description=request.data.get('description',journal_instance.description)


    journal_instance.save()

    return Response({"msg":" journal updated successfully"},status=200)



@api_view(['DELETE'])
def journal_delete(request,id):
    journal_delete=Journal.objects.filter(id=id).delete()
    
    if not journal_delete:
        return Response({"journal_delete does not deleted"},status=400)
    else:
        return Response({"journal deleted Successfully"},status=200)
    

import csv

##csv##
def journal_export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['code','journal_name','type','description'])


    for j in Journal.objects.all():
        writer.writerow([
            j.code,j.journal_name,j.type,j.description
        ])

   

    response['content-Disposition'] = 'attachment; filename="journal.csv"'   

    return response

##journalentry##

@api_view(['POST'])
def journalentry_create(request):
    serializer = journalentrySerializer(data=request.data)
    if serializer.is_valid():
        journal_entry =serializer.save()
        return Response({
            "msg":"journal entry created successfully",
            "id":journal_entry.id
        },status=201)
    else:
        return Response(serializer.errors,status=400)

@api_view(['GET'])
def journalentry_details(request):
    journals = JournalEntry.objects.all()
    serializer =journalentrySerializer(journals,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def journal_entry_details(request):
    try:
        journalentry_details= JournalEntry.objects.all()

        if not journalentry_details:
            return Response({"journalentry_details is not found"},status=400)
        
        entry_details=[]
        for edata in journalentry_details:
            entry_details.append({
                "id":edata.id,
                "reference":edata.reference,
                "accounting_date":edata.accounting_date,
                "journal":edata.journal.id,
                "description":edata.description,
                "status":edata.status

            })
        return Response(entry_details,status=200)
    except Exception as e:
        return Response({"msg":"journalentry is created {str:{e}}"},status=400)
        

@api_view(['DELETE'])
def journal_entry_delete(request,id):
    deleted =JournalEntry.objects.filter(id=id).delete()
    if not deleted:
        return Response({"msg":"journalentry does not deleted"},status=400)
    else:
        return Response({"msg":"journalentry delete successfully"},status=200)


##journal items##
@api_view(['GET'])
def journal_items_details(request):
    items= JournalItems.objects.all()
    serializer =JournalItemsSerializer(items,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def JournalItems_detail(request):
    try:
        details = JournalItems.objects.all()

        if not details:
            return Response ({"msg":"JournalItems details is not found"},status=200)
        

        Items=[]
        for data in details:
            Items.append({
                "id":data.id,
                "account":data.account.id,
                "partner":data.partner,
                "label":data.label,
                "debit":data.debit,
                "credit":data.debit
            
            })
        return Response(Items,status=200)
        
    except Exception as e:
        return Response({"msg":"journal details is {str:{e}}"},status=400)    


@api_view(['DELETE'])
def  journal_items(request,id):
    items_deleted = JournalItems.objects.filter(id=id).delete()
    if not items_deleted:
        return Response({"journal items not  deleted"},status=400)
    else:
        return Response({"journal item deleted successfully"},status=200) 



##trila balance##

def trial_balance():
    account =Account.objects.all()
    
    trial_balance =[]
    total_debits =Decimal("0.00")
    total_credits =Decimal("0.00")

    for acc in account:
        debit =JournalItems.objects.filter(account=acc).aggregate(total=Sum('debit'))['total'] or (Decimal('0.00'))
        credit =JournalItems.objects.filter(account=acc).aggregate(total =Sum('credit'))['total'] or (Decimal('0.00'))

        balance = debit - credit

        if balance > 0:
            trial_balance.append({"account":acc.name, 'debit':balance, "credit":Decimal("0.00")})
            total_debits += balance
        else:
            trial_balance.append({'account':acc.name,"debit":Decimal('0.00'),'credit':abs(balance)})
            total_credits -= balance

    return {
        "rows":trial_balance,
        "total_debits":total_debits,
        "total_creditd":total_credits
        }



@api_view(['GET'])
def trial_balance_view(request):
    DATA =trial_balance()
    return Response(DATA)

@api_view(['GET'])
def genaral_ledger(request,id):

    items =(JournalItems.objects.filter(account_id=id).select_related("journalentry").order_by("journalentry__accounting_date",'id'))

    ledger = []

    running_balance = 0
    for line in items:
        debit = line.debit or 0
        credit =line.credit or 0
        running_balance += debit - credit
        ledger.append({
            "date":line.journalentry.accounting_date,
            "reference":line.journalentry.reference,
            "partner" : line.partner,
            "label":line.label,
            "debit":line.debit,
            "credit":line.credit,
            "balance":running_balance

        })
    return Response(ledger,status=200)




@api_view(['POST'])
def create_customer(request):
    name = request.data.get("name")
    email =request.data.get("email")
    phone= request.data.get("phone")
    address= request.data.get("address")
    City= request.data.get("City")
    state= request.data.get("state")
    Country=request.data.get("Country")
    Zip_code = request.data.get("Zip_code")
    status = request.data.get("status")
    gstin = request.data.get("gstin")
    pan = request.data.get("pan")
    tax_id = request.data.get("tax_id")
    credit_limit = request.data.get("credit_limit")
    notes= request.data.get("notes")
    website = request.data.get("website")

    if customers.objects.filter(email=email).exists():
        return Response({"msg":"email is already exists"},status=400)

    

    create_customers= customers.objects.create(
        name=name,
        email= email,
        phone=phone,
        address=address,
        City=City,
        state=state,
        Country=Country,
        Zip_code=Zip_code,
        status=status,
        gstin=gstin,
        pan=pan,
        tax_id=tax_id,
        credit_limit=credit_limit,
        notes=notes,
        website =website

    )
    create_customers.save()

    return Response({"msg":"customer create sucessfully"},status=200)


@api_view(['GET'])
def customers_list(request):
    list =customers.objects.all()
    serializer = customersSerializer(list,many=True)
    return Response(serializer.data)



##customer details##
@api_view(['GET'])
def customer_details(request):
    try:
        details = customers.objects.all()

        if not details:
            return Response ({"msg":"customer details is not found"},status=200)
        

        dev=[]
        for data in details:
            dev.append({
                "id":data.id,
                "name":data.name,
                "email":data.email,
                "status":data.status,
                "phone":data.phone,
                "current_balance":data.current_balance,
            
            })
        return Response(dev,status=200)
        
    except Exception as e:
        return Response({"msg":"customer details is {str:{e}}"},status=400)    

    
@api_view(["PUT"])
def customer_update(request,email):

    customer_instance =customers.objects.filter(email=email).first()
    if not customer_instance:
        return Response({"msg":"customer data is not updated"},status=400)
    
    customer_instance.name =request.data.get('name',customer_instance.name)
    customer_instance.email=request.data.get('email',customer_instance.email)
    customer_instance.phone=request.data.get('phone',customer_instance.phone)
    customer_instance.address=request.data.get('address',customer_instance.address)
    customer_instance.City=request.data.get('City',customer_instance.City)
    customer_instance.state=request.data.get('state',customer_instance.state)
    customer_instance.Country=request.data.get('Country',customer_instance.Country)
    customer_instance.Zip_code=request.data.get('Zip_code',customer_instance.Zip_code)
    customer_instance.status=request.data.get('status',customer_instance.status)
    customer_instance.gstin=request.data.get('gstin',customer_instance.gstin)
    customer_instance.pan=request.data.get('pan',customer_instance.pan)
    customer_instance.tax_id=request.data.get('tax_id',customer_instance.tax_id)
    customer_instance.credit_limit=request.data.get('credit_limit',customer_instance.credit_limit)
    customer_instance.notes=request.data.get('notes',customer_instance.notes)
    customer_instance.website=request.data.get('website',customer_instance.website)

    customer_instance.save()

    return Response({"msg":"updated successfully"},status=200)


@api_view(['DELETE'])
def customer_delete(request,name):
    customer_deleted=customers.objects.filter(name=name).first()
    customer_deleted.delete()
    
    if not customer_deleted:
        return Response({"customer does not deleted"},status=400)
    else:
        return Response({"customer deleted Successfully"},status=200)
    


#csv#
def customer_export(request):
    response =HttpResponse(content_type='text/csv')

    response['content-Disposition'] ='attachment; filename="customer.csv"'

    writer =csv.writer(response)
    writer.writerow(['name','email','phone','address','City','state','Country','Zip_code','status','gstin','pan','tax_id','credit_limit','notes','website']) 

    for cust in customers.objects.all():
            writer.writerow([cust.name,cust.email,cust.phone,cust.address,cust.City,cust.state,cust.Country,cust.Zip_code,cust.status,cust.gstin,cust.pan,cust.tax_id,cust.credit_limit,cust.notes,cust.website]) 

    return response


@api_view(['POST'])
def create_customercontact(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        job_title = request.data.get('job_title')
        notes = request.data.get('notes')

        contact = customer_contact.objects.create(
            name =name,
            email=email,
            phone= phone,
            job_title=job_title,
            notes =notes
            
        )

        contact.save()

        return Response({"msg":"contact create sucessfully"},status=200)
    
    except Exception as e:
        return Response({"msg":"contact created as {str:{e}}"},status=400)

@api_view(['GET'])
def contact_details(request):
    contact = customer_contact.objects.all()
    if not contact :
        return Response({"msg":"contact details is not found"},status=400)

    contacts =[]


    for cont in contact:
        contacts.append({
            "name":cont.name,
            "email":cont.email,
            "phone":cont.phone,
            "job_title":cont.job_title


        })
    return Response(contacts,status=200)

@api_view(['PUT'])
def contact_update(request,id):
    contact_instance= customer_contact.objects.filter(id=id).first()
    if not contact_instance:
        return Response({'msg':'contact data not found'},status=400)
    
    contact_instance.name = request.data.get('name',contact_instance.name)
    contact_instance.email = request.data.get('email',contact_instance.email)
    contact_instance.phone =request.data.get('phone',contact_instance.phone)
    contact_instance.job_title= request.data.get('job_title',contact_instance.job_title)
    contact_instance.notes = request.data.get('notes',contact_instance.notes)

    contact_instance.save()

    return Response({'msg':"contact update sucessfully"},status=200)



@api_view(['DELETE'])
def contact_delete(request,id):
    deleted = customer_contact.objects.filter(id=id).delete()
    if not deleted:
        return Response({"msg":"customer_contact is not deleted"},status=400)
    
    return Response({"msg":"customer_contact is deleted successfully"},status=200)

# #customer balance for single customer
# @api_view(['POST'])
# def update_customer_balance(request,id):
#     try:
#        customer =customers.objects.get(id=id)
#     except customers.DoesNotExist:
#         return Response ({"detail":"customer not found"},status=400) 

#     old_balance = customer.current_balance
#     customer.update_balance()

#     return Response({
#         'old_balance': float(old_balance or 0),
#         'new_balance': float(customer.current_balance or 0),
#         'message': 'Customer balance updated successfully'
#     })  

#  #customer all balance
# @api_view(['POST'])
# def update_all_customer_balance(request):
#     customer =customers.objects.all()
#     for cust in customer:
#         cust.update_balance()

#         return Response({"msg": f"updated{customer.count()} current balances"})



@api_view(['POST'])
def product_create(request):
    Name= request.data.get('Name')
    sales= request.data.get('sales')
    purchase =request.data.get('purchase')
    product_type = request.data.get('product_type')
    price = request.data.get('price')
    description = request.data.get('description')

    product_create = product.objects.create(
        Name=Name,
        sales= sales,
        purchase =purchase,
        product_type = product_type,
        price =price,
        description=description
    )

    product_create.save()

    if not product_create:
        return Response({"msg":"product does not created"},status=400)

    return Response ({"msg":"product create successfully"},status=200)


@api_view(['GET'])
def product_view(request):
    product_details = product.objects.all()

    if not product_details:
        return Response({'product details not found'},status=400)
    list=[]
    for prod in product_details:
        list.append({
            "id":prod.id,
            "name":prod.Name,
            "price":prod.price
        })
    return Response(list,status=200)
    

@api_view(['PUT'])
def product_update(request,Name):
    product_instance= product.objects.filter(name=Name).first()
    if not product_instance:
        return Response({"msg":"produt does not found"},status=400)
    
    product_instance.Name = request.data.get('Name',product_instance.Name)
    product_instance.sales = request.data.get('sales',product_instance.sales)
    product_instance.purchase= request.data.get('purchase',product_instance.purchase)
    product_instance.product_type = request.data.get('product_type',product_instance.product_type)
    product_instance.price = request.data.get('price',product_instance.price)
    product_instance.description = request.data.get('description',product_instance.description)

    product_instance.save()

    return Response({"product update successfully"},status=200)


@api_view(['DELETE'])
def product_delete(request,Name):
    product_deleted = product.objects.filter(name=Name).delete()
    if not product_deleted:
        return Response({"msg":"product does not delete"},status=400)
    else:
        return Response({"msg":"product delete successfully"},status=200)

@api_view(['POST'])
def invoice_create(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        invoice = serializer.save()
        return Response({
            "msg": "Invoice entry created successfully",
            "id": invoice.id
        }, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def invoice_details(request):
    invoice =salesInvoice.objects.all()

    if not invoice:
        return Response({"msg":"invoice is not display"},status=400)
    
    invoices=[]
    for inv in invoice:
        invoices.append({
            "customer":inv.customer.name,
            "invoice_Date":inv.invoice_Date,
            "Due_Date":inv.Due_Date,
            "payments_terms":inv.payments_terms,
            "Status":inv.Status,
            "total":inv.total,
            "journals":inv.journals.journal_name if inv.journals else None

        })

    return Response(invoices,status=200)

@api_view(['GET'])
def invoice_list(request):
    list =salesInvoice.objects.all()
    serializer = InvoiceSerializer(list,many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def invoice_update(request,id):
    invoice_instance = salesInvoice.objects.filter(id=id).first()
    if not invoice_instance:
        return Response({"msg":"invoice not found"},status=400)
    
    customer_id = request.data.get('customer')
    if customer_id is not None:
        customer_instance = customers.objects.filter(id=customer_id).first()
        if not customer_instance:
            return Response({"msg":"customer id is not found"},status=400)    
        invoice_instance.customer = customer_instance

    journal_id = request.data.get('journals')
    if journal_id is not None:
        journal_instance =Journal.objects.filter(id=journal_id).first()
        if not journal_instance:
            return Response({"msg":"journal id is not found"},status=400)
        invoice_instance.journals =journal_instance

    invoice_instance.invoice_Date =request.data.get("invoice_Date",invoice_instance.invoice_Date)
    invoice_instance.Due_Date = request.data.get("Due_Date",invoice_instance.Due_Date)
    invoice_instance.payments_terms = request.data.get("payments_terms",invoice_instance.payments_terms)
    invoice_instance.Status = request.data.get("Status",invoice_instance.Status)

    invoice_instance.save()

    return Response({"msg":"invoice updated sucessfully"},status=201)
    

@api_view(['DELETE'])
def invoice_delete(request,id):
    invoice_deleted =salesInvoice.objects.filter(id =id).delete()
    if not invoice_deleted:
        return Response({"msg":"invoice is not deleted"},status=400)
    return Response({"msg":"invoice sucessfully deleted"},status=200)

@api_view(['POST'])
def payment_create(request):
    serializer =customer_paymentsSerializer(data=request.data)
    if serializer.is_valid():
        payment =serializer.save()
        return Response({
            "msg":"payments create sucessfully",
            "id":payment.id

        },status=201)
    return Response(serializer.errors,status=400)


@api_view(['PUT'])
def payment_update(request,id):
    payment_instance = customer_payment.objects.filter(id=id).first()
    if not payment_instance:
        return Response({"msg":"payment not update "},status=400)
    
    customer_id = request.data.get('customer')
    if customer_id is not None:
        customer_instance = customers.objects.filter(id=customer_id).first()
        if not customer_instance:
            return Response({"msg":"customer id is not found"},status=400)    
        payment_instance.customer = customer_instance

    invoice_id =request.data.get('invoice')
    if invoice_id is not None:
        invoice_instance = salesInvoice.objects.filter(id=invoice_id).first()
        if not invoice_instance:
            return Response({"msg":"invoice id is not found"},status=400)
        payment_instance.invoice =invoice_instance    

    journal_id = request.data.get('journal')
    if journal_id is not None:
        journal_instance =Journal.objects.filter(id=journal_id).first()
        if not journal_instance:
            return Response({"msg":"journal id is not found"},status=400)
        payment_instance.journal =journal_instance

    payment_instance.payment_date =request.data.get("payment_date",payment_instance.payment_date)
    payment_instance.amount = request.data.get("amount",payment_instance.amount)
    payment_instance.reference = request.data.get("reference",payment_instance.reference)
    payment_instance.status = request.data.get("status",payment_instance.status)

    payment_instance.save()

    return Response({"msg":"payment updated sucessfully"},status=201)
    

@api_view(['DELETE'])
def payment_delete(request,id):
    payment_deleted =customer_payment.objects.filter(id =id).delete()
    if not payment_deleted:
        return Response({"msg":"payment is not deleted"},status=400)
    return Response({"msg":"payment sucessfully deleted"},status=200)



## //vendor// ##
@api_view(['POST'])
def vendor_create(request):
    name = request.data.get("name")
    Company_name=request.data.get("Company_name")
    email =request.data.get("email")
    phone=request.data.get("phone")
    Category= request.data.get("Category")
    address = request.data.get("address")
    city =request.data.get("city")
    state=request.data.get("state")
    zipcode =request.data.get("zipcode")
    country=request.data.get("country")
    tax_id=request.data.get("tax_id")
    payment = request.data.get("payment")
    current_balance=request.data.get("current_balance")
    status=request.data.get("status")
    notes=request.data.get("notes")
    
    create_vendor = vendor.objects.create(
    name =name,
    Company_name=Company_name,
    email=email,
    phone=phone,
    Category=Category,
    address=address,
    city=city,
    state=state,
    zipcode=zipcode,
    country=country,
    tax_id=tax_id,
    payment=payment,
    current_balance=current_balance,
    status=status,
    notes=notes
    )
    create_vendor.save()

    return Response({"msg":"vendor create sucessfully"},status=200)


@api_view(['GET'])
def vendor_details(request):
    try:
        vendor_details = vendor.objects.all()

        if not vendor_details:
            return Response ({"msg":"vendor details is not found"},status=200)
        

        ven=[]
        for data in vendor_details:
            ven.append({
                "id":data.id,
                "name":data.name,
                "email":data.email,
                "category":data.Category,
                "status":data.status,
                "phone":data.phone,
                "current_balance":data.current_balance,
            
            })
        return Response(ven,status=200)
        
    except Exception as e:
        return Response({"msg":"vendor details is {str:{e}}"},status=400)    


    
@api_view(["PUT"])
def vendor_update(request,email):

    vendor_instance =vendor.objects.filter(email=email).first()
    if not vendor_instance:
        return Response({"msg":" vendor data is not updated"},status=400)
    
    vendor_instance.name =request.data.get('name',vendor_instance.name)
    vendor_instance.Company_name=request.data.get('Company_name',vendor_instance.Company_name)
    vendor_instance.email=request.data.get('email',vendor_instance.email)
    vendor_instance.phone=request.data.get('phone',vendor_instance.phone)
    vendor_instance.Category=request.data.get('Category',vendor_instance.Category)
    vendor_instance.address=request.data.get('address',vendor_instance.address)
    vendor_instance.city=request.data.get('city',vendor_instance.city)
    vendor_instance.state=request.data.get('state',vendor_instance.state)
    vendor_instance.zipcode=request.data.get('zipcode',vendor_instance.zipcode)
    vendor_instance.country=request.data.get('country',vendor_instance.country)
    vendor_instance.tax_id=request.data.get('tax_id',vendor_instance.tax_id)
    vendor_instance.payment=request.data.get('payment',vendor_instance.payment)
    vendor_instance.current_balance=request.data.get('current_balance',vendor_instance.pan)
    vendor_instance.status=request.data.get('status',vendor_instance.status)
    vendor_instance.notes=request.data.get('notes',vendor_instance.notes)


    vendor_instance.save()

    return Response({"msg":"updated successfully"},status=200)


@api_view(['DELETE'])
def vendor_delete(request,name):
    vendor_deleted=vendor.objects.filter(name=name).first()
    vendor_deleted.delete()
    
    if not vendor_deleted:
        return Response({"customer does not deleted"},status=400)
    else:
        return Response({"customer deleted Successfully"},status=200)




#productvendor
@api_view(['POST'])
def vendor_product_create(request):
    Name= request.data.get('Name')
    sales= request.data.get('sales')
    purchase =request.data.get('purchase')
    product_type = request.data.get('product_type')
    price = request.data.get('price')
    description = request.data.get('description')

    product_create = vendor_product.objects.create(
        Name=Name,
        sales= sales,
        purchase =purchase,
        product_type = product_type,
        price =price,
        description=description
    )

    product_create.save()

    if not product_create:
        return Response({"msg":" vendor product does not created"},status=400)

    return Response ({"msg":" vendor product create successfully"},status=200)


@api_view(['GET'])
def vendor_product_view(request):
    product_details = vendor_product.objects.all()

    if not product_details:
        return Response({' vendor product details not found'},status=400)
    list=[]
    for prod in product_details:
        list.append({
            "id":prod.id,
            "name":prod.Name,
            "price":prod.price
        })
    return Response(list,status=200)
    

@api_view(['PUT'])
def vendor_product_update(request,id):
    product_instance= vendor_product.objects.filter(id=id).first()
    if not product_instance:
        return Response({"msg":" vendor produt does not found"},status=400)
    
    product_instance.Name = request.data.get('Name',product_instance.Name)
    product_instance.sales = request.data.get('sales',product_instance.sales)
    product_instance.purchase= request.data.get('purchase',product_instance.purchase)
    product_instance.product_type = request.data.get('product_type',product_instance.product_type)
    product_instance.price = request.data.get('price',product_instance.price)
    product_instance.description = request.data.get('description',product_instance.description)

    product_instance.save()

    return Response({" vendor product update successfully"},status=200)


@api_view(['DELETE'])
def vendor_product_delete(request,id):
    product_deleted = vendor_product.objects.filter(id=id).delete()
    if not product_deleted:
        return Response({"msg":" vendor product does not delete"},status=400)
    else:
        return Response({"msg":"vendor product delete successfully"},status=200)



@api_view(['POST'])
def vendor_invoice_create(request):
    serializer = purchaseinvoiceSerializer(data=request.data)
    if serializer.is_valid():
        invoice = serializer.save()
        return Response({
            "msg": "vendor Invoice entry created successfully",
            "id": invoice.id
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def vendor_invoice_display(request):
    purinvoice =purchaseinvoice.objects.all()

    if not purinvoice:
        return Response({"msg":"vendorinvoice is not display"},status=400)
    
    vendores=[]
    for ven in purinvoice:
        vendores.append({
            "vendor":ven.vendor,
            "invoice_Date":ven.invoice_Date,
            "Due_Date":ven.Due_Date,
            "payments_terms":ven.payments_terms,
            "Status":ven.Status,
            "total":ven.total,
            "journals":ven.journals

        })

        return Response(vendores,status=200)
    

@api_view(['DELETE'])
def vendorinvoice_delete(request,id):
    invoice_delete =purchaseinvoice.objects.filter(id=id).delete()
    if not invoice_delete:
        return Response({"msg":"vendor invoice not deleted"})
    return Response({"msg":"vendor invoice delete successfully"},status=200)

@api_view(['POST'])
def vendor_payment_create(request):
    serializer =vendor_paymentSerializer(data=request.data)
    if serializer.is_valid():
        payment =serializer.save()
        return Response({
            "msg":"vendor payments create sucessfully",
            "id":payment.id

        },status=201)
    return Response(serializer.errors,status=400)


@api_view(['GET'])
def vendor_payment_details(request):
    vendor_details =vendor_payment.objects.all()

    dispaly=[]
    for dis in vendor_details:
        dispaly.append({
            "vendors":dis.vendors,
            "invoice":dis.invoice,
            "payment_date":dis.payment_date,
            "amount":dis.amount,
            "journal":dis.journal,
            "reference":dis.reference,
            "status":dis.status
        })

    return Response(dispaly,status=200)


@api_view(['DELETE'])
def vendor_payment_delete(request,id):
    vendor_pay_delete = vendor_payment.objects.filter(id=id).delete()
    if not vendor_pay_delete:
        return Response({"msg":"vendor payment not delete"},status=400)
    
    return Response({"msg":"vendor payment delete successfully"},status=200)


#dashboard

@api_view(['GET'])
def total_revenue(request):
    total = salesInvoice.objects.aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
    return Response({"total_revenue": total}, status=200)

@api_view(['GET'])
def total_Expense(request):
    total = purchaseinvoice.objects.aggregate(total_expense=Sum('total'))['total_expense'] or 0
    return Response({"total_expense": total}, status=200)

@api_view(['GET'])
def total_netprofit(request):
    total_revenue = salesInvoice.objects.aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
    total_expense = purchaseinvoice.objects.aggregate(total_expense=Sum('total'))['total_expense'] or 0
    net_profit = total_revenue - total_expense
    return Response({"net_profit": net_profit}, status=200)

@api_view(['GET'])
def total_Products(request):
    total = product.objects.count()
    return Response({"total_products": total}, status=200)

@api_view(['GET'])
def total_Customers(request):
    total = customers.objects.count()
    return Response({"total_customers": total}, status=200)

@api_view(['GET'])
def total_Vendors(request):
    total = vendor.objects.count()
    return Response({"total_vendors": total}, status=200)

@api_view(['GET'])
def recent_invoices(request):
    invoices = salesInvoice.objects.order_by('-invoice_Date')[:5]
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def recent_payments(request):
    payments = customer_payment.objects.order_by('-payment_date')[:5]
    serializer = customer_paymentsSerializer(payments, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def recent_vendor_invoices(request):
    vendor_invoices = purchaseinvoice.objects.order_by('-invoice_Date')[:5]
    serializer = purchaseinvoiceSerializer(vendor_invoices, many=True)
    return Response(serializer.data, status=200)
@api_view(['GET'])
def recent_vendor_payments(request):
    vendor_payments = vendor_payment.objects.order_by('-payment_date')[:5]
    serializer = vendor_paymentSerializer(vendor_payments, many=True)
    return Response(serializer.data, status=200)

#



