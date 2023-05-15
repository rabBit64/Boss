const payDataTag = document.querySelector('#pay_data')
const productPk = payDataTag.dataset.productPk
const count = payDataTag.dataset.count

let popupWindow

// 팝업 띄우기
function openPopup() {
  const popupWidth = 660;
  const popupHeight = 760;
  const left = (window.innerWidth / 2) - (popupWidth / 2)
  const top = (window.innerHeight / 2) - (popupHeight / 2)
  
  popupWindow = window.open(`/kakaopay/pay_product/${productPk}/${count}/`, 'pay_product', `fullscreen=1, width=${popupWidth}, height=${popupHeight}, top=${top}, left=${left}, location=no, status=yes, scrollbars=yes`)
  
  checkIfPopupIsClosed()
}

// 팝업이 닫혔는지 확인
function checkIfPopupIsClosed() {
  const checkInterval = setInterval(function() {
    if (popupWindow && popupWindow.closed) {
      clearInterval(checkInterval);
      window.location = `/boss/${productPk}/` // 상품 상세 페이지로 이동
    }
  }, 1000);
}

// 팝업 띄우기 실행
window.onload = function() {
  openPopup()
}