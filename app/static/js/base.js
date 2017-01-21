(function ($) {
  $(document).ready(function(){

    $("#header").headroom();
    $('.logofield').click(function() {
        window.location.href = '/';
    });
});
  }(jQuery));
