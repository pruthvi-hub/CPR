from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None: # Check if the user is found in db
            auth.login(request,user)
            messages.success(request,"You are now logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('index')

def register(request):
    if request.method == 'POST':
       # Get form values
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       confirm_password  = request.POST['confirm_password']

       # Check if passwords match
       if password == confirm_password:
           # Check if the username in db is equal to the input username 
           if User.objects.filter(username=username).exists():
               messages.error(request, 'That username is already taken!')
               return redirect('register')
           else:
                # Check if the email in db is equal to the input email 
               if User.objects.filter(email=email).exists():
                   messages.error(request, 'That email is already being used!')
                   return redirect('register') 
               else:
                   # Register the user
                   user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                   user.save()
                   messages.success(request,'You are now registered and can log in!')
                   return redirect('login')
                   # Login right after registration
                #    auth.login(request,user)
                #    messages.success(request,'You are now logged in!')
                #    return redirect('login')

       else:
           messages.error(request , 'Passwords do not match!')
           return redirect('register')
    else:
         return render(request,'accounts/register.html')

def dashboard(request):

    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
    

