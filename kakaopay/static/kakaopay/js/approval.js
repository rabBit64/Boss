const dataTag = document.getElementById('payment')
cartId = dataTag.dataset.cartId
userName = dataTag.dataset.userName

$(document).ready(function() {
  $('#close-popup').click(function() {
    window.close()
    window.opener.location.href = `/accounts/profile/${userName}`
  }); // 결제 성공시 닫기버튼 누르면 프로필 화면으로 이동 // 나중에 주문페이지로 이동으로 변경
});
