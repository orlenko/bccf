$.cergis = $.cergis || {};
$.cergis.loadContent = function () {
    $('.ajax-loader').show();
    $.ajax({
        url: pageUrl + '?type=ajax',
        success: function (data) {
            $('#slide-content').html(data);
            console.log("test2");
            // hide ajax loader
            $('.ajax-loader').hide();
        }
    });
    if (pageUrl != window.location) {
        window.history.pushState({ path: pageUrl }, '', pageUrl);
    }
    console.log("test3");
}
$.cergis.backForwardButtons = function () {
    $(window).on('popstate', function () {
        $.ajax({
            url: location.pathname + '?type=ajax',
            success: function (data) {
                $('#main-content').html(data);
            }
        });
    });
}
$('.content-header').on('click', function(e) {
    if(!$(this).hasClass('content-header-active')) { // was the active one clicked?
        reset();
        pageUrl = $(this).attr('href');
        $.cergis.loadContent();
        $(this).addClass('content-header-active');
        $('#slide-content-container').fadeIn(500);
    } else {
        reset();
    }
    e.preventDefault();
});
$.cergis.backForwardButtons();
