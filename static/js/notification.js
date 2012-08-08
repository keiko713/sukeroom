/*
<!-- notification -->
<div class="notification hide">
  <span class="notify-text">追加しました</span>
</div>
<!-- /notification -->
*/
/* show notification and hide in 5 sec */
$(function() {
  $('.notification').show();
  setTimeout(notiFadeout, 3000);
  function notiFadeout() {
    $('.notification').fadeOut("slow");
  }
  $('.notification').click(function() {
    notiFadeout();
  });
});
