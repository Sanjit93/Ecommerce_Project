from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistartionFrom, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#def home(request):
 #return render(request, 'ShopApp/home.html')
class ProductView(View):
 def get(self,request):
  bottomwears= Product.objects.filter(category='BW')
  topwears = Product.objects.filter(category='TW')
  mobile = Product.objects.filter(category='M')
  return render(request,'ShopApp/home.html',{'bottomwears':bottomwears,'topwears':topwears,'mobile':mobile})


#def product_detail(request):
 #return render(request, 'ShopApp/productdetail.html')
class ProductDetailView(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  return render(request,'ShopApp/productdetail.html',{'product':product})

def add_to_cart(request,):
 user=request.user
 product_id= request.GET.get('prod_id')
 print("b")
 product= Product.objects.get(id=product_id)
 print("c")
 Cart(user=user,product=product).save()
 print(('D'))
 return redirect('/cart')

def show_cart(request):
 if request.user.is_authenticated:
  user=request.user
  cart=Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=70
  total_amount=0.0
  cart_product=[p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount=(p.quantity * p.product.discounted_price)
    amount+=tempamount
    totalamount=amount+shipping_amount

   return render(request, 'ShopApp/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
   return render(request,'ShopApp/emptycart.html')

def plus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
   totalamount = amount + shipping_amount
  data={
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':totalamount,
   }
  return JsonResponse(data)

def minus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
   totalamount = amount + shipping_amount
  data={
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':totalamount,
   }
  return JsonResponse(data)
@login_required
def remove_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

  c.delete()
  amount = 0.0
  shipping_amount = 70
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
   totalamount = amount + shipping_amount
  data={

   'amount':amount,
   'totalamount':totalamount,
   }
  return JsonResponse(data)



def buy_now(request):
 return render(request, 'ShopApp/buynow.html')

#def profile(request):
 #return render(request, 'ShopApp/profile.html')
method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  form =CustomerProfileForm()
  return render(request,'ShopApp/profile.html',{'form':form,'active':'btn-primary'})
 def post(self,request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   usr  =  request.user
   name =  form.cleaned_data["name"]
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'profile has been updated')
  return render(request, 'ShopApp/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'ShopApp/address.html',{'add':add,'active':'btn-primary'})
@login_required
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'ShopApp/orders.html',{'order_placed':op})

def change_password(request):
 return render(request, 'ShopApp/changepassword.html')

def mobile(request,data=None):
 if data==None:
  mobiles=Product.objects.filter(category='M')
 elif data=='Apple' or data=='Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data=='Vivo' or data=='motorola':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data=='below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=40000)
 elif data=='above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=40000)
 return render(request,'ShopApp/mobile.html',{'mobiles':mobiles})

def Bottom_Wear(request,data=None):
 if data==None:
  bottomwears=Product.objects.filter(category='BW')
 elif data=='Men' or data=='Women':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)

 return render(request,'ShopApp/btwears.html',{'bottomwears':bottomwears})

def Top_Wear(request,data=None):
 if data==None:
  topwears=Product.objects.filter(category='TW')
  return render(request, 'ShopApp/tpwears.html', {'topwears': topwears})

#def login(request):
 #return render(request, 'ShopApp/login.html')

#def customerregistration(request):
# return render(request, 'ShopApp/customerregistration.html')

class CustomerRegistartionView(View):
  def get(self,request):
   form = CustomerRegistartionFrom()
   return render(request,'ShopApp/Customerregistration.html',{'form':form })
  def post(self,request):
   form = CustomerRegistartionFrom(request.POST)
   if form.is_valid():
    messages.success(request,'congratulation!! you have registered successfully')
    form.save()
   return render(request, 'ShopApp/Customerregistration.html', {'form': form})

@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  totalamount = amount + shipping_amount

 return render(request, 'ShopApp/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect("orders")
