$(document).ready(function() {
  $('#close-popup').click(function() {
    window.close()
    window.opener.location.href = '/cart/'
  })
})