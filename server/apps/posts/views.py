from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post

# Create your views here.
def main(request):
  # 쿼리스트링 가져오기
  search_txt = request.GET.get('search_txt')
  min_price = request.GET.get('min_price')
  max_price = request.GET.get('max_price')

  posts = Post.objects.all()
  # SELECT * FROM posts_posts;
  # 필터링

  if search_txt:
    posts = posts.filter(title__contains=search_txt)
  if min_price:
    posts = posts.filter(price__gt=min_price)
  if max_price:
    posts = posts.filter(price__lt=max_price)
  
  ctx = {'posts': posts}
  return render(request, 'posts/post_list.html', ctx) 

def create(request):
  if request.method == 'GET':
    form = PostForm()
    ctx = {'form': form}
    return render(request , 'posts/post_create.html', ctx)
  
  # POST일때
  form = PostForm(request.POST, request.FILES)
  if form.is_valid():
    form.save()
  return redirect('posts:main')

def detail(request, pk):
  post = Post.objects.get(id=pk)
  user = post.user # 정참조
  related_posts = user.post_set.all() # 역참조
  ctx = {'post': post, 'related_posts': related_posts}
  return render(request, 'posts/post_detail.html', ctx)

def delete(request, pk):
  if request.method == 'POST':
    # pk에 해당하는 Post 객체 조회하는 방법
    # posts = Post.objects.get(id=pk)
    # posts.delete()
    Post.objects.get(id=pk).delete()
  return redirect('posts:main')

def update(request, pk):
  post = Post.objects.get(id=pk)
  
  if request.method == 'GET':
    form = PostForm(instance=post)
    ctx = {'form': form, 'pk': pk}
    return render(request, 'posts/post_update.html', ctx)
  
  form = PostForm(request.POST, request.FILES, instance=post)
  if form.is_valid():
    form.save()
  return redirect('posts:detail', pk)