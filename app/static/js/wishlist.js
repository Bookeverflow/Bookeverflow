(function ($) {
  $(document).ready(function(){
      $('.wishitem').click(function() {
          id = $(this).data('id');
          $.ajax({
              type: 'POST',
              url: '/deletewish/' + id,
              success: function() {
                  notie().alert(1, 'Success removed', 2.5);
                  setTimeout(function() {location.reload();}, 500);
              },
              error: function(xhr, status, error) {
                  notie().alert(3, error, 2.5);
              }
          });
      });
  });
}(jQuery));
