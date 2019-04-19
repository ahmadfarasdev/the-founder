from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, UserVote, Comment
from .forms import CommentForm
from django.utils import timezone
from django.core.mail import EmailMessage

# Create your views here.

def homepage(request):
    products = Product.objects.order_by('votes_total')
    return render(request, 'products/home.html', {'products': products})

@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            # Saves into database
            product.save()
            return redirect('/products/' + str(product.id))
    else:
        return render(request, 'products/create.html', {'error': 'All fields are required'})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.all().order_by('id')

    form = CommentForm()

    return render(request, 'products/detail.html', {
        'product': product,
        'form': form,
        'comments': comments
    })

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        user_vote, new_vote = UserVote.objects.get_or_create(user=request.user, product=product)

        if new_vote:
            product.votes_total += 1
            product.save()

            # Send mail
            email = EmailMessage(
                subject='test',
                body='test',
                from_email='diaforetikus@gmail.com',
                to=[product.hunter.email],
            )

            email.content_subtype = "html"  # Main content is now text/html
            email.send()

        return redirect('/products/' + str(product.id))

@login_required(login_url='/accounts/signup')
def comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        form = CommentForm(request.POST)

        if form.is_valid():
            Comment.objects.create(
                product=product,
                user=request.user,
                message=form.cleaned_data['message']
            )

        return redirect('/products/' + str(product.id))