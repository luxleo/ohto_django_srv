from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,get_user
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import PostForm
from .models import Tag,Post

# Create your views here.
@login_required
def post_new(req):
    if req.method == 'POST':
        form = PostForm(req.POST,req.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(req,'포스팅 생성완료 했다')
            #reverse url 쓰기 위해서 model단에서 get_absolute_url사용해야한다.
            return redirect(post)
    else:
        form = PostForm()
    return render(req,'instagram/post_form.html',{
        "form":form
    })

def post_detail(req,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(req,'instagram/post_detail.html',{
        "post":post
    })

def user_page(req,user_name):
    page_user = get_object_or_404(get_user_model(),username=user_name,is_active=True)
    post_list = Post.objects.filter(author = page_user)
    return render(req,'instagram/user_page.html',{
        "page_user":page_user,
        "post_list" : post_list
    })
