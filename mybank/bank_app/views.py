from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Credential,Customer,Transaction,contact_us
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import Signup, Transfor,Login_form,Customer_Contactus
# from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.models import User

# Create your views here.
# from django.conf.urls import url

def read_data():
    with open('/Users/prakashyadava/Downloads/Bank 3/find_details.txt','r') as f:
        data = f.read()
    js = json.loads(data)
    return js
def write_data(gen_data):
    with open('/Users/prakashyadava/Downloads/Bank 3/find_details.txt','w') as f:
        f.write(json.dumps(gen_data))

def generate_customer_id_acc_id():
    gen_data = read_data()
    cust_id = "DDB" + str(gen_data['cust_id'])
    gen_data['cust_id'] = gen_data['cust_id'] + 1
    acc_no = gen_data['acc_no']
    gen_data['acc_no'] = gen_data['acc_no'] +1
    write_data(gen_data)
    return cust_id,acc_no

def generate_transaction_id():
    gen_data = read_data()
    trans_id = "TRANS" + str(gen_data['trans'])
    gen_data['trans'] = gen_data['trans'] + 1
    write_data(gen_data)
    return trans_id
#..............................................


def index(request):
    return redirect('bankapp/')

def landingpage(request):
    if request.method == 'POST':
        form = Customer_Contactus(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact_details = contact_us(name=name,email=email,message=message)
            contact_details.save()
            messages.success(request,f'Hi {name}, we will contact you shortly!')
            return redirect(landingpage)
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 
            return redirect(landingpage)
    else:
        form = Customer_Contactus()
        return render(request,'landingpage.html',{'form':form})
    # return render(request,'landingpage.html')



def getcustid(cust_id):
    return cust_id

# def mylogin(request):

#     if request.method=='POST':
#         cust_id = request.POST.get('cust_id')
#         password = request.POST.get('password')
#         customers = Credential.objects.all().values()
#         print(cust_id,password)
#         for cust in customers:
#             if cust['customer_id_id']==cust_id and cust['password']==password:
#                 return redirect(test,cust_id)
#     return render(request,'mylogin.html')

    # if request.method=='POST':
    #     cust_id = request.POST.get('cust_id')  # change1
    #     #cust_id = request.POST['cust_id']
    #     #password = request.POST['password']
    #     password = request.POST.get('password')   #change1
    #     customers = Credential.objects.all().values()
    #     if unhash_password(cust_id,password):
    #         messages.info(request,"successfully loggedin")
    #         return redirect(test,cust_id)
    #     else:
    #         return HttpResponse("chuitya devloper agar nahi kar paye toh")
                
    # return render(request,'mylogin.html')
    
@login_required(login_url='bankapp/test/<cust_id>')
def test(request,cust_id):
    if request.method =='POST':
        customers = Customer.objects.all().values()
        transactions = Transaction.objects.all().values()
        trans_form = Transfor(request.POST)
        if trans_form.is_valid():
            transfer_to_account_no = trans_form.cleaned_data['transfer_to']
            amount = trans_form.cleaned_data['amount']
            flag = False
            trans_flag = False
            this_cust = None
            trans_cust = None
            for customer in customers:
                if customer['account_number'] == transfer_to_account_no:
                    trans_flag = True
                    break

            for customer in customers:
                if customer['customer_id'] == cust_id and int(customer['Balance'])>= int(amount):
                    this_cust = customer
                    flag = True
                    break
            if flag and trans_flag:
                s_ac = ""
                gen_trans_id = generate_transaction_id()
                for customer in customers:
                    if customer['customer_id']==cust_id:
                        Customer.objects.filter(customer_id = customer['customer_id']).update(Balance = str(int(customer['Balance']) - int(amount)))
                        s_ac = customer['account_number']
                        new_amount = "-"+ amount
                        transaction = Transaction(customer_id_id = this_cust['customer_id'],transaction_id = gen_trans_id+'S',transaction_amount = new_amount,transaction_account =transfer_to_account_no)
                        transaction.save()
                        break
                for customer in customers:
                    if customer['account_number']==transfer_to_account_no:
                        trans_cust = customer
                        Customer.objects.filter(customer_id = customer['customer_id']).update(Balance = str(int(customer['Balance']) + int(amount)))
                        new_new_amt = "+" + amount
                        transaction = Transaction(customer_id_id = trans_cust['customer_id'],transaction_id = gen_trans_id+'R',transaction_amount =new_new_amt,transaction_account = s_ac)
                        transaction.save()
                        break

                return HttpResponse('paise chale gaye bhai')
            else:
                if not trans_flag:
                    return HttpResponse('bhai account sahi daal le')
                elif not flag:
                    return HttpResponse('paise kama le bhai')
                
    else:    
        trans_form = Transfor()
        data = Customer.objects.get(pk = cust_id)
        trans_all_data = Transaction.objects.all().values()
        trans_data = []
        for dt in trans_all_data:
            temp = []
            if dt['customer_id_id']== cust_id:
                
                temp.append(dt['customer_id_id'])
                temp.append(dt['transaction_id'])
                temp.append(dt['transaction_account'])
                temp.append(dt['transaction_amount'])
                trans_data.append(temp)
            
        context = {'data':data,'trans_form': trans_form,'trans_data':trans_data}
        return render(request,'test.html',context)

def mysignup(request):
    if request.method =='POST':
        
        reg = Signup(request.POST)
        if reg.is_valid():
            first_name = reg.cleaned_data['first_name']
            middle_name = reg.cleaned_data['middle_name']
            last_name = reg.cleaned_data['last_name']
            resident_addr = reg.cleaned_data['resident_addr']
            office_addr = reg.cleaned_data['office_addr']
            phone_no = reg.cleaned_data['phone_no']
            email = reg.cleaned_data['email']
            password = reg.cleaned_data['password']
            repassword = reg.cleaned_data['repassword']
            Balance = reg.cleaned_data['Balance']
            # password = hash_password(password)
            get_data = generate_customer_id_acc_id()
            cust_id = get_data[0]
            acc_no = get_data[1]
            user = User.objects.create_user(username=cust_id,password=password)
            user.save()
            cust = Customer(customer_id = cust_id,account_number=acc_no,first_name=first_name,middle_name=middle_name,last_name=last_name,resident_address=resident_addr,office_address=office_addr,phone_number=phone_no,email=email,Balance=Balance)
            cust.save()
            cred = Credential(customer_id =cust,password = password)
            cred.save()
            messages.success(request,cust_id)
            return redirect(mylogin)
            # change redirect to login page
        else:
            return redirect(landingpage)
    else:
        reg = Signup()

        return render(request,'mysignup.html',{'reg':reg})




#...................after logged in methods............................


def logoutpage(request):
    logout(request)
    return redirect(mylogin)
    # return render(request,'landingpage.html')
#...................using django forms............................

def mylogin(request):
    # if request.user.is_authenticated:
    #     return redirect(landingpage) 
    if request.method=='POST':
        form = Login_form(request.POST)
        if form.is_valid():
            cust_id = form.cleaned_data['cust_id']
            password = form.cleaned_data['password']
            user = authenticate(username = cust_id, password = password)
            if user is not None:
                login(request,user)
                return redirect("test",cust_id)
                
            else:
                return HttpResponse('user not found')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 
            return HttpResponse('hi form not valid')


        # for cust in customers:
        #     if cust['customer_id_id']==cust_id and cust['password']==password:
        #         return redirect(test,cust_id)
    else:
        form = Login_form()
        for error in list(form.errors.values()):
                messages.error(request, error)
        return render(request,'mylogin.html',{'form':form})