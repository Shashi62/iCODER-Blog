from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# HTML pages
def home(request):
    # return HttpResponse('This is home.....')
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    # messages.success(request, 'Welcome to contact')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4 :
            messages.error(request, 'Please fill the form correctly')
        else : 
            contact = Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, 'Your messages has been successfully sent')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78 :
        allPosts = Post.objects.none()
    else :
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
            messages.warning(request, 'No search results found. Please redefine your query')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous input
        # Username should be under 10 characters
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        # Username should contain only letters and numbers
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        # Password must be same
        if pass1 != pass2 :
            messages.error(request, "Password do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.firstname = fname
        myuser.lastname = lname
        myuser.save()
        messages.success(request, "Your iCODER account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')           

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameter
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')

        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')


    return HttpResponse('404 - Not Found')           

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')


        