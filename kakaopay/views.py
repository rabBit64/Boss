from django.shortcuts import render, redirect
import requests
import os
from dotenv import load_dotenv
load_dotenv()
KAKAO_AK = os.getenv('KAKAO_AK')

# Create your views here.
def index(request):
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + KAKAO_AK,   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "item_name": "연어초밥",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "12000",        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": f'http://127.0.0.1:8000/kakaopay/pay_success/', # 결제 승인시 이동할 url # 카트아이디
            "cancel_url": f'http://127.0.0.1:8000/kakaopay/pay_fail/', # 결제 취소 시 이동할 url
            "fail_url": f'http://127.0.0.1:8000/kakaopay/pay_cancel/', # 결제 실패 시 이동할 url
        }

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)

    return render(request, 'kakaopay/index.html')


def kakaopay(request):
    pass

def pay_success(request, product_pk):
      product = Product.objects.get(pk=product_pk)
      url = 'https://kapi.kakao.com/v1/payment/approve'
      admin_key = KAKAO_AK
      
      headers = {
          'Authorization': f'KakaoAK {admin_key}'
      }
      data = {
          'cid':'TC0ONETIME',
          'tid': request.session['tid'], #결제 고유 번호
          'partner_order_id': product.pk, #주문 번호
          'partner_user_id': request.user.username, #유저 아이디
          'pg_token': request.GET['pg_token'] 
      }
      res = requests.post(url, data=data, headers=headers)
      result = res.json()
      context = {
          'res':res,
          'result':result,
      }
      if result.get('msg'): #msg = 오류 코드
          return redirect('products:pay_fail')
      else:
          product.purchase_users.add(request.user, through_defaults={
              'title': product.title,
              'count': result['quantity'],
              'price': result['amount']['total']
          })
          return render(request, 'products/pay_success.html', context)


def pay_fail(request):
    return render(request, 'products/pay_fail.html')

def pay_cancel(request):
    return render(request, 'products/pay_cancel.html')