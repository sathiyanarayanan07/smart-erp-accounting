from django.shortcuts import render
from rest_framework.response import Response
from .models import role1,QA,Admin,accountent,product,product_details,plan_product,product_material,product_details
from .models import product_options,schedule,account_page,schedule_process
from rest_framework import status
from .serializers  import role1Serializer,product_detailsSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.
@api_view(['POST'])
def single_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role_type = request.data.get("role_type")

    if not username or not password or not role_type:
        return Response("user not found")
    try:
        if role_type == "role1":
            role1_login = role1.objects.get(username=username,password=password,role_type=role_type)
        elif role_type == "QA":
            Qa_login = QA.objects.get(username=username,password=password,role_type=role_type)
        elif role_type == "product":
            product_login = product.objects.get(username=username,password=password,role_type=role_type)
        elif role_type == "Admin":
            Admin_login = Admin.objects.get(username=username,password=password,role_type=role_type)
        elif role_type == "accountent":
            accountent_login = accountent.objects.get(username=username,password=password,role_type=role_type)
        else:
            return Response({"msg":"invalid user"})
        
    except (role1.DoesNotExist, QA.DoesNotExist, product.DoesNotExist,
            Admin.DoesNotExist, accountent.DoesNotExist):
        return Response({"msg": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

    # Login successful
    return Response({
        "msg": "Login successful",
        "username": username,
        "role_type": role_type
    }, status=status.HTTP_200_OK)


permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user_data(request):
    get_data =role1.objects.all()

    get=[]
    for gets in get_data:
        get.append({
            "username":gets.username,
            "password":gets.password,
        })
    return Response(get)

@api_view(['POST'])
def admin_single_signup(request):
    username =request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    role_type =request.data.get("role_type")



    email_exists = (
        role1.objects.filter(email=email).exists() or
        QA.objects.filter(email=email).exists() or
        product.objects.filter(email=email).exists() or
        Admin.objects.filter(email=email).exists() or
        accountent.objects.filter(email=email).exists()
    )

    if email_exists:
        return Response({"msg": "Email already exists"}, status=400)
 
    try:
        if role_type =="role1":
            role = role1.objects.create(username=username,email=email,password=password,role_type=role_type)
        elif role_type == "QA":
            role2 = QA.objects.create(username=username,email=email,password=password,role_type=role_type)
        elif role_type == "product":
            role3 = product.objects.create(username=username,email=email,password=password,role_type=role_type)
        elif role_type == "Admin":
            role2 = Admin.objects.create(username=username,email=email,password=password,role_type=role_type)
        elif role_type == "accountent":
            role2 = accountent.objects.create(username=username,email=email,password=password,role_type=role_type)
        else:
            return Response({"msg":"invaild data"},status=200)
        
    except (role1.DoesNotExist, QA.DoesNotExist, product.DoesNotExist,
            Admin.DoesNotExist, accountent.DoesNotExist):
        return Response({"msg": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

    # Login successful
    return Response({
        "msg": "signup successful",
        "username": username,
        "email":email,
        "password":password,
        "role_type": role_type
    }, status=200 )   

@api_view(['POST'])
def logout(request):
    username = request.data.get('username')
    role_type = request.data.get("role_type")

    if not username or not role_type:
        return Response ({"msg":"username and roletype is not found"},status=200)
    
    if role_type == "role1":
        role_1 = role1.objects.get(username=username)
    elif role_type == "QA":
        qa = QA.objects.get(username=username)
    elif role_type == "product":
        product_logout = product.objects.get(username=username)
    elif role_type == "Admin":
        admin = Admin.objects.get(username=username)
    elif role_type == "accountent":
        account = accountent.objects.get(username=username)
    else:
        return Response({"logout not successfully "},status=400)
    return Response({
    "msg":"logout successfully",
    "username":username,
    "role_type":role_type
    })

#product add in role 1

@api_view(['POST'])
def add_product_details(request):
    Company_name=request.data.get("Company_name")
    serial_number=request.data.get("serial_number")
    date=request.data.get("date")
    Customer_name=request.data.get("Customer_name")
    Customer_No=request.data.get("Customer_No")
    Customer_date=request.data.get("Customer_date")
    mobile =request.data.get("mobile")
    status=request.data.get("status")

    try:
        product_data=product_details.objects.create(
            Company_name=Company_name,
            serial_number=serial_number,
            date=date,
            Customer_name=Customer_name,
            Customer_No=Customer_No,
            Customer_date=Customer_date,
            mobile=mobile,
            status="pending"
        )
    except product_details.DoesNotExist:
        return Response({"msg":"invalid data"},status=status.HTTP_400_BAD_REQUEST)
    return Response({
        "msg":"data added successfully",
        "Company_name":Company_name,
        "serial_number":serial_number,
        "date":date,
        "Customer_name":Customer_name,
        "Customer_No":Customer_No,
        "Customer_date":Customer_date,
        "mobile":mobile,
        "status":"pending"
    },status=200)



    
@api_view(['PUT'])
def update_product_status(request, id):
    product_instance = product_details.objects.get(id=id)

    if not product_instance:
        return Response({"msg": "No data found"}, status=status.HTTP_404_NOT_FOUND)
    
    product_instance.Company_name = request.data.get('Company_name', product_instance.Company_name)
    product_instance.serial_number = request.data.get('serial_number', product_instance.serial_number)
    product_instance.date = request.data.get('date', product_instance.date)
    product_instance.Customer_name = request.data.get('Customer_name', product_instance.Customer_name)
    product_instance.Customer_No = request.data.get('Customer_No', product_instance.Customer_No)
    product_instance.Customer_date = request.data.get('Customer_date', product_instance.Customer_date)
    product_instance.mobile = request.data.get('mobile', product_instance.mobile)
    product_instance.status = request.data.get('status', product_instance.status)
    product_instance.save()
    serializer = product_detailsSerializer(product_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)

    

@api_view(['DELETE'])
def delete_product(request, id):
    product_instance = product_details.objects.get(id=id).delete()

    if not product_instance:
        return Response({"msg": "No data found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({"msg": "data deleted"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_product_material(request):
    product_id =request.data.get("product_detail")
    material_Description =request.data.get("material_Description")
    Quantity =request.data.get("Quantity")
    Remarks =request.data.get("Remarks")
    try:
        product = product_details.objects.get(id=product_id)
        product_material_data=product_material.objects.create(
            product_detail=product,
            material_Description=material_Description,
            Quantity=Quantity,
            Remarks=Remarks
        )
    except product_details.DoesNotExist:
        return Response({"msg":"invalid product id"},status=404)
    return Response({
        "msg":"Product material added successfully",
    },status=200)
    
@api_view(['GET'])
def get_product_materials(request):
    product_material_data = product_material.objects.all()
    get = []
    for material in product_material_data:
        get.append({
            "product_detail": material.product_detail.id if material.product_detail else None,
            "material_Description": material.material_Description,
            "Quantity": material.Quantity,
            "Remarks": material.Remarks,
        })
    return Response(get)

@api_view(['POST'])
def add_product_options(request):
    product_id = request.data.get("product_Material")
    size= request.data.get("size")
    Thick= request.data.get("Thick")
    Grade= request.data.get("Grade")
    Drawing= request.data.get("Drawing")
    Test_Certificate= request.data.get("Test_Certificate")

    try:
        product_material_instance = product_material.objects.get(id=product_id)
        product_options_data = product_options.objects.create(
            product_material=product_material_instance,
            size=size,
            Thick=Thick,
            Grade=Grade,
            Drawing=Drawing,
            Test_Certificate=Test_Certificate
        )
    except product_material.DoesNotExist:
        return Response({"msg": "Invalid product material ID"}, status=404)
    return Response({
        "msg": "Product options added successfully",
    }, status=200)


@api_view(['GET'])
def get_product_options(request):
    product_options_data = product_options.objects.all()
    get = []
    for option in product_options_data:
        get.append({
            "product_Material": option.product_material.id if option.product_material else None,
            "size": option.size,
            "Thick": option.Thick,
            "Grade": option.Grade,
            "Drawing": option.Drawing,
            "Test_Certificate": option.Test_Certificate,
        })
    return Response(get)


#qa views to qa page

@api_view(['GET'])
def qa_view(request):
    product_data=product_details.objects.all()
    get=[]
    for products in product_data:
        get.append({
        
            "Company_name":products.Company_name,
            "serial_number":products.serial_number,
            "status":products.status,
            
        })
    return Response(get)


@api_view(['POST'])
def add_plan_product(request):
    product_id = request.data.get("product_detail")
    program_no = request.data.get("program_no")
    lm_co1 = request.data.get("lm_co1")
    lm_co2 = request.data.get("lm_co2")
    lm_co3 = request.data.get("lm_co3")
    fm_co1 = request.data.get("fm_co1")
    fm_co2 = request.data.get("fm_co2")
    fm_co3 = request.data.get("fm_co3")

    
    try:
        product = product_details.objects.get(id=product_id)
    except product_details.DoesNotExist:
        return Response({"msg": "Invalid product ID"}, status=404)
    
    plan_data = plan_product.objects.create(
        product_detail=product,
        program_no=program_no,
        lm_co1=lm_co1,
        lm_co2=lm_co2,
        lm_co3=lm_co3,
        fm_co1=fm_co1,
        fm_co2=fm_co2,
        fm_co3=fm_co3,
    )

    return Response({
        "msg": "data added successfully",
        "product_detail": product_id,
        "program_no": program_no,
        "lm_co1": lm_co1,
        "lm_co2": lm_co2,
        "lm_co3": lm_co3,
        "fm_co1": fm_co1,
        "fm_co2": fm_co2,
        "fm_co3": fm_co3,
        "status": product.status
    }, status=200)

@api_view(['GET'])
def get_plan_products(request):
    plan_data = plan_product.objects.all()
    get = []
    for plan in plan_data:
        get.append({
            "product_detail": plan.product_detail.id if plan.product_detail else None,
            "program_no": plan.program_no,
            "lm_co1": plan.lm_co1,
            "lm_co2": plan.lm_co2,
            "lm_co3": plan.lm_co3,
            "fm_co1": plan.fm_co1,
            "fm_co2": plan.fm_co2,
            "fm_co3": plan.fm_co3,
        })
    return Response(get)    


# product page
@api_view(['POST'])
def Schedule_add(request):
    product_id=request.data.get("product_plan")
    commitment_date = request.data.get("commitment_date")
    planning_date = request.data.get("planning_date")
    date_of_inspection = request.data.get("date_of_inspection")
    date_of_delivery = request.data.get("date_of_delivery")
    
    
    schedule_add = schedule.objects.create(
        product_plan= product_id,
        commitment_date= commitment_date,
        planning_date =planning_date,
        date_of_inspection = date_of_inspection,
        date_of_delivery= date_of_delivery,
       
    )

    return Response({"msg":"product schedule create successfully",
                     "product_plan":product_id,
                     "commitment_Date":commitment_date,
                     "planning_date":planning_date,
                     "date_of_delivery":date_of_delivery,
                     "date_of_inspection":date_of_inspection,
                  
                   },status=200)




# product page
@api_view(['POST'])
def Schedule_process(request):
    schedule_id=request.data.get("schedule_name")
    process =request.data.get("process")
    process_date = request.data.get("process_date")
    cycle_time = request.data.get("cycle_time")
    operator_name = request.data.get("operator_name")
    remark = request.data.get("remark")
    
    try:
        schedules = schedule.objects.get(id=schedule_id)
    except schedule.DoesNotExist:
        return Response({"error": "Schedule not found."},
                        status=status.HTTP_404_NOT_FOUND)
    
    schedule_add = schedule_process.objects.create(
        schedule_name=schedules,
        process = process,
        process_date= process_date,
        cycle_time =cycle_time,
        operator_name = operator_name,
        remark= remark,
       
    )
    
    return Response({"msg":"process schedule create successfully",
                     "schedules_name":schedules.id,
                     "process_date":process_date,
                     "cycle_time":cycle_time,
                     "operator_name":operator_name,
                     "remark":remark,
                  
                   },status=200)
@api_view(['GET'])
def Schedule_view(request):
    schedules = schedule.objects.all()

    if not schedules.exists():
        return Response({"msg": "No schedule data found"}, status=400)

    schedule_list = []

    for sched in schedules:
        # Fetch all related schedule_process for this schedule
        processes = schedule_process.objects.filter(schedule_name=sched)

        process_list = []
        for proc in processes:
            process_list.append({
                "plan_product": proc.product_plan.id if proc.product_plan else None,
                "process": proc.process,
                "process_date": proc.process_date,
                "cycle_time": proc.cycle_time,
                "operator_name": proc.operator_name,
                "remark": proc.remark
            })

        schedule_list.append({
            "commitment_date": sched.commitment_date,
            "planning_date": sched.planning_date,
            "date_of_delivery": sched.date_of_delivery,
            "date_of_inspection": sched.date_of_inspection,
            "processes": process_list  # nested processes
        })

    return Response({
        "msg": "Schedule data retrieved successfully",
        "schedules": schedule_list
    }, status=200)


@api_view(['GET'])
def Schedule_view(request):
    try:
        schedules = schedule.objects.all()

        if not schedules.exists():
            return Response({"msg": "No schedule data found"}, status=404)

        response_data = []
        for sch in schedules:
            # Fetch all related process records for this schedule
            processes = schedule_process.objects.filter(schedule_name=sch)

            # Build nested process data
            process_data = [
                {
                    "schedule_name":p.schedule_name.id,
                    "process_date": p.process_date,
                    "cycle_time": p.cycle_time,
                    "operator_name": p.operator_name,
                    "remark": p.remark,
                }
                for p in processes
            ]

            # Add schedule + its processes
            response_data.append({
                "product_plan":sch.product_plan.id,
                "commitment_date": sch.commitment_date,
                "planning_date": sch.planning_date,
                "date_of_inspection": sch.date_of_inspection,
                "date_of_delivery": sch.date_of_delivery,
                "process_details": process_data,
            })

        return Response(response_data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def product_qa_view(request):
    prod_view = product_details.objects.all()
    if not prod_view:
        return Response({"msg":"prod not found"},status=400)
    
    qa_view =plan_product.objects.all()
    if not qa_view:
        return Response({"msg":"qa not found"},status=400)
    
    schedule_view =schedule.objects.all()
    if not schedule_view:
        return Response({"data not found schedule_view"})
   
        
    schedule_view_process = schedule_process.objects.all()
    if not schedule_view_process :
        return Response({"schedule_view_process not found"})


    
    prod = []
    for ve in prod_view:
        prod.append({
        "Company_name":ve.Company_name,
        "serial_number":ve.serial_number,
        "date":ve.date,
        "Customer_name":ve.Customer_name,
        "Customer_No":ve.Customer_No,
        "Customer_date":ve.Customer_date,
        "mobile":ve.mobile,
        "status":ve.status
            

        })

    qa_details = []
    for qv in qa_view:
        qa_details.append({
            "program_no": qv.program_no,
            "lm_co1": qv.lm_co1,
            "lm_co2": qv.lm_co2,
            "lm_co3": qv.lm_co3,
            "fm_co1": qv.fm_co1,
            "fm_co2": qv.fm_co2,
            "fm_co3": qv.fm_co3,
            "status":qv.status
        })

    view=[]
    for show in schedule_view:
        view.append({
                    "product_plan":show.product_plan.id,
                    "commitment_Date":show.commitment_date,
                    "planning_date":show.planning_date,
                    "date_of_delivery":show.date_of_delivery,
                    "date_of_inspection":show.date_of_inspection,
                
                })
    sdl=[]
    for pro in schedule_view_process:
        sdl.append({
            "schedule_name":pro.schedule_name.id,
            "process":pro.process,
            "process_date":pro.process_date,
            "cycle_time":pro.cycle_time,
            "operator_name":pro.operator_name,
            "remark":pro.remark
        })

    
    return Response({"msg":"all details view successfully",
                    "product":prod,
                    "qa":qa_details,
                    "Schedule_View":view,
                    "Schedule process":sdl
                    })


#account

@api_view(['POST'])
def add_account(request):
    inv_on = request.data.get("inv_on")
    Date = request.data.get("Date")
    Amount = request.data.get("Amount")
    mode_of_pay = request.data.get("mode_of_pay")
    mat_inspected = request.data.get("mat_inspected")
    mat_received = request.data.get("mat_received")
    process_plan = request.data.get("process_plan")
    process_approve = request.data.get("process_approve")
    remark = request.data.get("remark")

    if not inv_on or not Date or not Amount or not mode_of_pay or not mat_inspected or not mat_received or  not process_plan or not process_approve or not remark:
        return Response({"msg":"data not found"})
    
    acc = account_page.objects.create(
        inv_on=inv_on,
        Date=Date,
        Amount=Amount,
        mode_of_pay=mode_of_pay,
        mat_inspected=mat_inspected,
        mat_received=mat_received,
        process_plan=process_plan,
        process_approve=process_approve,
        remark=remark

    )
    return Response({
        "msg":"account page create successfully",
        "inv_on":inv_on,
        "Date":Date,
        "Amount":Amount,
        "mode_of_pay":mode_of_pay,
        "mat_inspected":mat_inspected,
        "mat_received":mat_received,
        "process_plan":process_plan,
        "process_approve":process_approve,
        "remark":remark
        },status=200)

@api_view(['GET'])
def account_view(request):
        view_detail =account_page.objects.all()

        if not view_detail:
            return Response({"msg":"data not found"},status=400)
        view=[]
        for show in view_detail:
                view.append({
                    "inv_on":show.inv_on,
                    "Date":show.Date,
                    "Amount":show.Amount,
                    "mode_of_pay":show.mode_of_pay,
                    "mat_inspected":show.mat_inspected,
                    "mat_received":show.mat_received,
                    "process_plan":show.process_plan,
                    "process_approve":show.process_approve,
                    "remark":show.remark
                })
        return Response(view)

#admin page
@api_view(['GET'])
def get_role_count(request):
    count_role =role1.objects.count()
    count_qa =QA.objects.count()
    count_product =product.objects.count()
    count_accountent=accountent.objects.count()
    return Response({"count":count_role,
                     "count_QA":count_qa,
                     "count_product":count_product,
                     "count_accountent":count_accountent
                     },status=200)

@api_view(['GET'])
def total_product(request):
    count_product=product_details.objects.count()
    return Response({"Total Product":count_product},status=200)  
           


@api_view(['GET'])
def over_all_details(request):
    product_details_qs = product_details.objects.all()
    product_options_qs = product_options.objects.all()
    plan_product_qs = plan_product.objects.all()
    schedule_qs = schedule.objects.all()
    schedule_process_qs = schedule_process.objects.all()
    account_page_qs = account_page.objects.all()
    product_material_qs = product_material.objects.all()

    product_details_list = [
        {
            "Company_name": pro.Company_name,
            "serial_number": pro.serial_number,
            "date": pro.date,
            "Customer_name": pro.Customer_name,
            "Customer_No": pro.Customer_No,
            "Customer_date": pro.Customer_date,
            "mobile": pro.mobile,
            "created_by":pro.created_by.username
        }
        for pro in product_details_qs
    ]


    product_material_list = [
        {
            "material_Description": mat.material_Description,
            "Quantity": mat.Quantity,
            "Remarks": mat.Remarks
        }
        for mat in product_material_qs
    ]
    
    product_options_list =[
        {
        "product_material":opt.product_material.id,
        "size":opt.size,
        "Thick":opt.Thick,
        "Grade":opt.Grade,
        "Drawing":opt.Drawing,
        "Test_Certificate":opt.Test_Certificate
        }
        for opt in product_options_qs
    ]

    plan_product_list =[
        {
        "product_detail":plan.product_detail.id,
        "program_no":plan.program_no,
        "lm_co1":plan.lm_co1,
        "lm_co2":plan.lm_co2,
        "lm_co3":plan.lm_co3,
        "fm_co1":plan.fm_co1,
        "fm_co2":plan.fm_co2,
        "fm_co3":plan.fm_co3,
        "status":plan.status,
        "created_by":plan.created_by.username

        }
        for plan in plan_product_qs
        ]
    schedule_list=[

        {
            "product_plan":sch.product_plan.id,
            "commitment_date":sch.commitment_date,
            "planning_date":sch.planning_date,
            "date_of_inspection":sch.date_of_inspection,
            "date_of_delivery":sch.date_of_delivery,
            "created_by":sch.created_by.username


        }
        for sch in schedule_qs
    ]

    schedule_process_list =[
        {
            "schedule_name":spro.schedule_name.id,
            "process_date":spro.process_date,
            "cycle_time":spro.cycle_time,
            "operator_name":spro.operator_name,
            "remark":spro.remark
        }
        for spro in schedule_process_qs

    ]

    account_page_list =[
        {
            "inv_on":acc.inv_on,
            "Date":acc.Date,
            "Amount":acc.Amount,
            "mode_of_pay":acc.mode_of_pay,
            "mat_inspected":acc.mat_inspected,
            "mat_received":acc.mat_received,
            "process_plan":acc.process_plan,
            "process_approve":acc.process_approve,
            "remark":acc.remark,
            "created_by":acc.created_by.username



        }
        for acc in account_page_qs

    ]

    response_data = {
        "product_details": product_details_list,
        "product_materials": product_material_list,
        "product_options": product_options_list,
        "plan_products": plan_product_list,
        "schedules": schedule_list,
        "schedule_processes": schedule_process_list,
        "account_pages": account_page_list
    }

    return Response(response_data)


      
  

      
      
      
