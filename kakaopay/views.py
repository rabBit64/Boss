from django.shortcuts import render, redirect
from cart.models import Cart
import requests
import os
from dotenv import load_dotenv
load_dotenv()
KAKAO_AK = os.getenv('KAKAO_AK')

# Create your views here.
def pay(request, cart_id):
    # if request.method == 'POST':
    # cart = Cart(request.session)
    cart = Cart.objects.get(cart_id=cart_id)
    for i in cart.cartitem_set.all():
        print('@@@@@@@@@@', i.product)
    
    cnt = 0
    cart_item = 'none'
    for item in cart.cartitem_set.all():
        cnt += 1
        if cnt == 1:
            cart_item = item.product.name
    # print(total_mount)
    print(cart.total_amount())
    if cnt > 1:
        cart_item += f' 외 {cnt-1} 건'
    print(cart_item)
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        'Authorization': 'KakaoAK ' + KAKAO_AK,   # 변경불가
        # 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',  # 변경불가
    }
    params = {
        'cid': 'TC0ONETIME',    # 테스트용 코드
        'partner_order_id': cart_id,     # 주문번호
        'partner_user_id': request.user.username, #request.user.username,    # 유저 아이디
        'item_name': cart_item,        # 구매 물품 이름
        'quantity': cnt,                # 구매 물품 수량
        'total_amount': cart.total_amount(),        # 구매 물품 가격
        'tax_free_amount': '0',         # 구매 물품 비과세
        'approval_url': f'http://127.0.0.1:8000/kakaopay/approval/{cart_id}', # 결제 승인시 이동할 url # 카트아이디
        'cancel_url': 'http://127.0.0.1:8000/kakaopay/pay_fail/', # 결제 취소 시 이동할 url
        'fail_url': 'http://127.0.0.1:8000/kakaopay/pay_cancel/', # 결제 실패 시 이동할 url
    }

    res = requests.post(URL, headers=headers, params=params)
    request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
    next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
    return redirect(next_url)


def approval(request, cart_id):
    cart = Cart.objects.get(cart_id=cart_id)
    print(cart)
    url = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        'Authorization': f'KakaoAK {KAKAO_AK}',
        # 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    params = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'], #결제 고유 번호
        'partner_order_id': cart_id, #주문 번호
        'partner_user_id': request.user.username, #유저 아이디
        'pg_token': request.GET['pg_token'] # 쿼리 스트링으로 받은 pg토큰
    }
    res = requests.post(url, headers=headers, params=params)
    # amount = res.json()['amount']['total']
    result = res.json()
    print(result)
    print(dir(result))
    # cart_items = cart.cartitem_set.all()
    # for cart_item in cart_items:
    #     cart_item.delete()
    context = {
        # 'res':res,
        'result': result,
        # 'amount': amount,
    }
    #   if result.get('msg'): #msg = 오류 코드
    #       return redirect('products:pay_fail')
    #   else:
    #       product.purchase_users.add(request.user, through_defaults={
    #           'title': product.title,
    #           'count': result['quantity'],
    #           'price': result['amount']['total']
    #       })
    return render(request, 'kakaopay/approval.html', context)


def pay_fail(request):
    return render(request, 'kakaopay/pay_fail.html')

def pay_cancel(request):
    return render(request, 'kakaopay/pay_cancel.html')

def wait(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(cart_id=cart_id) # 삭제
    
    context = {
        'cart': cart, # 삭제
        'cart_id': cart_id,
    }
    return render(request, 'kakaopay/wait.html', context)

# 안쓰는 코드
# def pay_finish(request, cart_id):
#     cart = Cart.objects.get(cart_id=cart_id)
#     cart_items = cart.cartitem_set.all()
#     # for cart_item in cart_items:
#     #     cart_item.delete()
#     print('finish로 오나?')
#     return redirect('accounts:profile', request.user.username)