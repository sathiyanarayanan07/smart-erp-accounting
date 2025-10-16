from django.db import models

# Create your models here.
class role1(models.Model):

    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    role_type = models.CharField(max_length=10,default="role1")

    def __str__(self):
        return f"{self.username} -{self.password}"
    
class QA(models.Model):

    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    role_type = models.CharField(max_length=10,default="QA")

    def __str__(self):
        return f"{self.username} -{self.password}"

    
class product(models.Model):

    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    role_type = models.CharField(max_length=10,default="product")

    def __str__(self):
        return f"{self.username} -{self.password}"
    
    
class accountent(models.Model):

    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    role_type = models.CharField(max_length=10,default="accountent")

    def __str__(self):
        return f"{self.username} -{self.password}"
    
    
class Admin(models.Model):

    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    role_type = models.CharField(max_length=10,default="Admin")

    def __str__(self):
        return f"{self.username} -{self.password}"

#product 
class product_details(models.Model):
    Company_name = models.CharField(max_length=30,null=True,blank=True)
    serial_number = models.CharField(max_length=30,null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    Customer_name = models.CharField(max_length=30,null=True,blank=True)
    Customer_No = models.CharField(max_length=30,null=True,blank=True)
    Customer_date = models.DateField(null=True,blank=True)
    mobile = models.CharField(max_length=30,null=True,blank=True)
    status=models.CharField(max_length=30,null=True,blank=True)
   

    def __str__(self):
        return f"{self.Company_name} -{self.serial_number}--{self.id}"
    
class product_material(models.Model):
    product_detail=models.ForeignKey(product_details,on_delete=models.CASCADE,null=True,blank=True)
    material_Description=models.CharField(max_length=100,null=True,blank=True)
    Quantity =models.IntegerField(null=True,blank=True)
    Remarks =models.CharField(max_length=100,null=True,blank=True)
    

    def __str__(self):
        return f"{self.material_Description} -{self.Quantity}--{self.id}"    
    
class product_options(models.Model):
    product_material=models.ForeignKey(product_material,on_delete=models.CASCADE,null=True,blank=True)
    size=models.BooleanField(max_length=30,null=True,blank=True)
    Thick=models.BooleanField(max_length=30,null=True,blank=True)
    Grade=models.BooleanField(max_length=30,null=True,blank=True)
    Drawing=models.BooleanField(max_length=30,null=True,blank=True)
    Test_Certificate=models.BooleanField(max_length=30,null=True,blank=True)
    def __str__(self):
        return f"{self.size} -{self.Thick}--{self.Grade}"

#qa
class plan_product(models.Model):
    product_detail=models.ForeignKey(product_details,on_delete=models.CASCADE,null=True,blank=True)
    program_no=models.CharField(max_length=30,null=True,blank=True)
    lm_co1=models.BooleanField(default=False)
    lm_co2=models.BooleanField(default=False)
    lm_co3=models.BooleanField(default=False)
    fm_co1=models.BooleanField(default=False)
    fm_co2=models.BooleanField(default=False)
    fm_co3=models.BooleanField(default=False)
    status = models.CharField(max_length=20,default="incomplete")

    def __str__(self):
        return f"{self.program_no}-{self.id}"
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product_detail:
            if any([
                self.lm_co1, self.lm_co2, self.lm_co3,
                self.fm_co1, self.fm_co2, self.fm_co3
            ]):
                self.product_detail.status = "complete"
            else:
                self.product_detail.status = "incomplete"
            self.product_detail.save()
            
   
    
#product
class schedule(models.Model):
    product_plan =models.ForeignKey(plan_product,on_delete=models.CASCADE)
    commitment_date = models.DateField(auto_now_add=False)
    planning_date = models.DateField(auto_now_add=False)
    date_of_inspection = models.DateField(auto_now_add=False)
    date_of_delivery = models.DateField(auto_now_add=False)
 


    def __str__(self):
        return f"Schedule on {self.commitment_date}--{self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product_plan:  
            if all([ self.commitment_date, self.planning_date, self.date_of_inspection, self.date_of_delivery]):
                self.product_plan.status = "complete"
            else:
                self.product_plan.status = "incomplete"

            self.product_plan.save()

#product_process  
class schedule_process(models.Model):
    schedule_name=models.ForeignKey(schedule,on_delete=models.CASCADE,null=True,blank=True)
    process =models.CharField(max_length=100,null=True,blank=True)
    process_date = models.DateField(auto_now_add=False)
    cycle_time = models.TimeField(null=True, blank=True)
    operator_name = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
   


                




    #account
class account_page(models.Model):
 
    inv_on = models.CharField(max_length=100,null=True,blank =True)
    Date = models.DateField(auto_now_add=True)
    Amount = models.DecimalField(max_length=100,null=True,blank=True,decimal_places=2,max_digits=10,default=0)
    mode_of_pay = models.CharField(max_length=20,null=True,blank=True)
    mat_inspected =models.CharField(max_length=100,null=True,blank=True)
    mat_received = models.CharField(max_length=100,null=True,blank=True)
    process_plan = models.CharField(max_length=100,null=True,blank=True)
    process_approve=models.CharField(max_length=100,null=True,blank=True)
    remark = models.CharField(max_length=50,null=True,blank=True)
    status =models.CharField(max_length=20,)

    def __Str__(self):
        return self.inv_on

