from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm


@login_required
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


# def login(request):
#     if request.user.is_authenticated:
#         return redirect('boss:index')

#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, request.POST)
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             return redirect('boss:index')
#     else:
#         form = CustomAuthenticationForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/login.html', context)

@login_required
def merge_cart(request):
    # 로그인 한 사용자의 장바구니
    user_cart, _ = Cart.objects.get_or_create(
        user=request.user,
        defaults={'cart_id': _cart_id(request)}
    )

    # 세션에 있는 장바구니
    session_cart = Cart.objects.get(cart_id=_cart_id(request))

    if session_cart.cartitem_set.exists():
        # 세션에 있는 장바구니를 사용자의 카트로 합치기
        for session_item in session_cart.cartitem_set.all():
            cart_item, created = CartItem.objects.get_or_create(
                product=session_item.product, cart=user_cart, defaults={'quantity': session_item.quantity}
            )

            if not created:
                cart_item.quantity += session_item.quantity
                cart_item.save()
        
        # 세션의 장바구니 삭제
        session_cart.delete()

    # 새로운 장바구니 ID를 로그인 한 사용자의 ID로 설정
    request.session['cart_id'] = str(user_cart.cart_id)

    return redirect('cart_detail')


def login(request):
    if request.user.is_authenticated:
        return redirect('boss:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth_authenticate(request, username=username, password=password)
            if user is not None:
                # 세션에 있는 장바구니
                try:
                    old_cart = Cart.objects.get(cart_id=_cart_id(request))
                except ObjectDoesNotExist:
                    old_cart = None
                auth_login(request, user)

                # 로그인 한 사용자의 장바구니
                try:
                    new_cart = Cart.objects.get(cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    new_cart = Cart.objects.create(cart_id = _cart_id(request))
                    new_cart.save()
                # 세션에 있는 장바구니를 사용자의 카트로 옮기기
                if old_cart is not None:
                    if old_cart.cartitem_set.exists():
                        for session_item in old_cart.cartitem_set.all():
                            cart_item, created = CartItem.objects.get_or_create(
                                product=session_item.product, cart=new_cart, defaults={'quantity': session_item.quantity}
                            )
                            if not created:
                                cart_item.quantity += session_item.quantity
                                cart_item.save()
                        # 세션의 장바구니 삭제
                        old_cart.delete()

                return redirect('boss:index')
            else:
                form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('boss:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('boss:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 세션에 있는 장바구니
            old_cart = Cart.objects.get(cart_id=_cart_id(request))
            
            auth_login(request, user)
            
            # 로그인 한 사용자의 장바구니
            try:
                new_cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                new_cart = Cart.objects.create(cart_id = _cart_id(request))
                new_cart.save()
            # 세션에 있는 장바구니를 사용자의 카트로 합치기
            if old_cart.cartitem_set.exists():
                for session_item in old_cart.cartitem_set.all():
                    cart_item, created = CartItem.objects.get_or_create(
                        product=session_item.product, cart=new_cart, defaults={'quantity': session_item.quantity}
                    )
                    if not created:
                        cart_item.quantity += session_item.quantity
                        cart_item.save()
                # 세션의 장바구니 삭제
                old_cart.delete()


            return redirect('boss:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('boss:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user
    if you == me:
        return redirect('accounts:profile', me.username)
    
    if me in you.followers.all():
        you.followers.remove(me)
    else:
        you.followers.add(me)

    return redirect('accounts:profile', you.username)