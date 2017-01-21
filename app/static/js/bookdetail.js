(function ($) {
  $(document).ready(function(){
    new QRCode(document.getElementById("qrcode"), window.location.href);
    $('.fb-share-link').attr('href', "https://www.facebook.com/sharer.php?u=" + window.location.href);

    if($(".actionBtn").data('nrequested')) {
        $(".actionBtn").click(function() {
            uuid = $(".actionBtn").data('uuid');
            $.ajax({
                type: 'POST',
                url: '/makedeal/' + uuid,
                success: function() {
                    notie().alert(3, 'Success added', 2.5);
                    setTimeout(function() {location.reload();}, 2000);
                },
                error: function(xhr, status, error) {
                    notie().alert(3, error, 2.5);
                }
            });
        });
    }
  });
}(jQuery));
