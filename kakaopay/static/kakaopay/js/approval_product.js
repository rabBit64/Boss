const dataTag = document.getElementById('payment')
productPk = dataTag.dataset.productPk

$(document).ready(function() {
  $('#close-popup').click(function() {
    window.close()
    window.opener.location.href = `/boss/${productPk}`
  }); // 결제 성공시 닫기버튼 누르면 상품페이지로 이동 // 나중에 주문페이지로 이동으로 변경
});
