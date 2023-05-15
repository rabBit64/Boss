$(document).ready(function() {
  $('#close-popup').click(function() {
    window.close()
    window.opener.location.href = '/cart/' // 닫기 버튼 누를 시 카트로 이동
  })
})