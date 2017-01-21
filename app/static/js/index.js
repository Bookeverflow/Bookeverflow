(function ($) {
  $(document).ready(function(){
      $('.recordwrapper').click(function(ele) {
          window.location.href = 'bookdetail/' + this.id;
      });
  });
}(jQuery));
