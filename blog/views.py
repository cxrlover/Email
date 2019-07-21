from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import EmailPostForm


# Create your views here.

def share_post(req, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if req.method == "POST":
        form = EmailPostForm(req.POST)
        if form.is_valid():
            # 获取数据,数据类型是字典
            cd = form.cleaned_data
            # 凑出一个完整的地址
            post_url = req.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(cd['name'],
                                                                  cd['email'],
                                                                  post.title)
            message = "Read'{}' at {}\n\n{}\'s comments:{}".format(post.title,
                                                                   post_url,
                                                                   cd['name'],
                                                                   cd['comments'])
            send_mail(subject, message, '1107849083@qq.com', [cd['to'],])
            sent = True
    else:
        form = EmailPostForm(req.POST)

    return render(req, 'blog/share.html', {'form': form,
                                           'post': post,
                                           })


# get没有访问到,则抛出404异常
# get_object_or_404

def post_list(req):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # posts = Post.published.all()
    # return render(req, 'blog/list.html', {'posts': posts})
    return render(req, 'blog/list.html', {'page': page, 'posts': posts})


def post_detail(req, year, month, day, post):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post, )
    return render(req, 'blog/detail.html', {'post': post})
