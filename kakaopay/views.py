from django.shortcuts import render, redirect
from cart.models import Cart
import requests
import os
from dotenv import load_dotenv
load_dotenv()
KAKAO_AK = os.getenv('KAKAO_AK')


# 결제창으로 연결
def pay(request, cart_id):
    cart = Cart.objects.get(cart_id=cart_id)
    current_site = request.build_absolute_uri()[:-34]
    cnt = 0
    cart_item = 'none'
    for item in cart.cartitem_set.all():
        cnt += 1
        if cnt == 1:
            cart_item = item.product.name
    if cnt > 1:
        cart_item += f' 외 {cnt-1} 건'

    URL = 'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        'Authorization': 'KakaoAK ' + KAKAO_AK,
    }
    params = {
        'cid': 'TC0ONETIME',    # 테스트용 코드
        'partner_order_id': cart_id,     # 주문번호
        'partner_user_id': request.user.username, # 유저 아이디
        'item_name': cart_item,        # 구매 물품 이름
        'quantity': cnt,                # 구매 물품 수량
        'total_amount': cart.total_amount(),        # 구매 물품 가격
        'tax_free_amount': '0',         # 구매 물품 비과세
        'approval_url': f'{current_site}/approval/{cart_id}', # 결제 승인시 이동할 url
        'cancel_url': f'{current_site}/pay_fail/', # 결제 취소 시 이동할 url
        'fail_url': f'{current_site}/pay_cancel/', # 결제 실패 시 이동할 url
    }

    res = requests.post(URL, headers=headers, params=params)
    request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
    next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
    return redirect(next_url)


# 결제 성공
def approval(request, cart_id):
    cart = Cart.objects.get(cart_id=cart_id)
    url = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        'Authorization': f'KakaoAK {KAKAO_AK}',
    }
    params = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'], #결제 고유 번호
        'partner_order_id': cart_id, #주문 번호
        'partner_user_id': request.user.username, #유저 아이디
        'pg_token': request.GET['pg_token'] # 쿼리 스트링으로 받은 pg토큰
    }
    res = requests.post(url, headers=headers, params=params)
    result = res.json()

    # 장바구니 비우기
    cart_items = cart.cartitem_set.all()
    for cart_item in cart_items:
        cart_item.delete()
    
    context = {
        'result': result,
    }
    
    return render(request, 'kakaopay/approval.html', context)


# 결제 실패
def pay_fail(request):
    return render(request, 'kakaopay/pay_fail.html')


# 결제 취소
def pay_cancel(request):
    return render(request, 'kakaopay/pay_cancel.html')


# 결제 대기
def wait(request):
    cart_id = request.POST.get('cart_id')
    
    context = {
        'cart_id': cart_id,
    }
    return render(request, 'kakaopay/wait.html', context)
