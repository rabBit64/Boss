const dataTag = document.getElementById('payment')
cartId = dataTag.dataset.cartId
// console.log(cartId)
userName = dataTag.dataset.userName

// $(".close").hide()
$(document).ready(function() {
  $('#close-popup').click(function() {
    window.close()
    window.opener.location.href = `/accounts/profile/${userName}`
  }); // 나중에 주문페이지로 연결
});

// document.addEventListener('DOMContentLoaded', function() {
//   const closePopupButton = document.getElementById('close-popup');
//   closePopupButton.addEventListener('click', function() {
//     window.close();
//     window.opener.location.reload();
//   });
// });