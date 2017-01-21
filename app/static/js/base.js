(function ($) {
  $(document).ready(function(){

    $("#header").headroom();
    $('.logofield').click(function() {
        window.location.href = '/';
    });
    $('.nav-btn').click(function() {
        $('nav').toggleClass('invisible');
    });
    $(window).scroll(function() {
        $('nav').addClass('invisible');
    });
});
  }(jQuery));
