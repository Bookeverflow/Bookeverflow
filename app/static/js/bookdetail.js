(function ($) {
  $(document).ready(function(){
    new QRCode(document.getElementById("qrcode"), window.location.href);
    $('.fb-share-link').attr('href', "https://www.facebook.com/sharer.php?u=" + window.location.href);
  });
}(jQuery));
