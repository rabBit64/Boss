const cartId = document.getElementById('payment').dataset.cartId
console.log(cartId)


$(document).ready(function() {
  $('#close-popup').click(function() {
    window.close();
    window.opener.location.href = `/kakaopay/pay_finish/${cartId}/`;
  });
});

// document.addEventListener('DOMContentLoaded', function() {
//   const closePopupButton = document.getElementById('close-popup');
//   closePopupButton.addEventListener('click', function() {
//     window.close();
//     window.opener.location.reload();
//   });
// });