const cartIdTag = document.querySelector('#pay_url')
const cartId = cartIdTag.dataset.cartId

window.onload = function() {
  openPopup()
}

function openPopup() {
  var popupWindow = window.open(`/kakaopay/${cartId}/`, 'pay', 'fullscreen=1, width=660, height=760, location=no, status=yes, scrollbars=yes');

  // 팝업이 닫혔는지 확인
  var checkPopupClosed = setInterval(function() {
    if (popupWindow.closed) {
      // 팝업이 닫힌 경우, 원래 페이지를 특정 URL로 이동한다.
      clearInterval(checkPopupClosed);
      window.location = '/cart/' // 특정 페이지 URL 추가
    }
  }, 1000);
}