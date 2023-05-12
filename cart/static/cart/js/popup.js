const popupBtn = document.querySelector('#pay_btn')
console.log(popupBtn)
const popupUrl = popupBtn.dataset.url
console.log(popupUrl)

function openPopup() {
  
  // 팝업을 연다
  var popupWindow = window.open(popupUrl, 'window_name', 'width=660, height=760, location=yes, status=yes, scrollbars=yes');

  // 팝업이 닫혔는지 확인
  var checkPopupClosed = setInterval(function() {
    console.log('@@@@@@@@@@@');
    if (popupWindow.closed) {
      // 팝업이 닫힌 경우, 원래 페이지를 특정 URL로 이동한다.
      clearInterval(checkPopupClosed);
      window.location = 'http://127.0.0.1:8000/boss/'; // 특정 페이지 URL 추가
    }
  }, 1000);
}