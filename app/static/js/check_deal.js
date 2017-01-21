(function ($) {
  $(document).ready(function(){

        $(".decisionBtn").click(function() {
            var uuid = $(this).data('uuid');
            var isaccept = $(this).data('accept') === 1;
            console.log('here');
            $.post('/makefinaldeal/' + uuid, {
                'accept': isaccept
            }).done(function() {
                notie().alert(3, 'Done', 2.5);
                setTimeout(function() {location.reload();}, 1000);
            }).fail(function(xhr, status, error) {
                notie().alert(3, error, 2.5);
            });
        });

    });
}(jQuery));
