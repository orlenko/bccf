var history_not_mobile = {
    'singleItem': true,
    'slideSpeed': 800,
    'paginationSpeed': 800,
    'rewindSpeed': 800,
    'pagination': false,
    'stopOnHover': true,
    'addClassActive': true,
    'autoPlay': false,
    'afterMove': function(elem) {
        elem.find('.history-image').hide();
        var $revealMe = elem.find('.active .history-image');
        var history_height = elem.find('.active .history-image').height();
        $revealMe.css({
            position: "relative",
            top: history_height+100,           
            height: 0
        }).delay(800).show().animate({
            top: 0,
            height: history_height
        }, {
            duration: 800,
            step: function(now, fx) {
                if (fx.prop == "top") {
                    $(fx.elem).scrollTop(now);
                }
            }
        });
     },
    'afterInit': function(elem) { elem.find('.active .history-image').show(); },
    'theme': 'history-theme',
}
var history_mobile = {
    'singleItem': true,
    'pagination': false,
    'autoPlay': 5000,
    'afterMove': null,
    'afterInit': function(elem) { elem.find('.history-image').show(); },
}
$(function(){
    $('#browse-by-nav').Flaunt();
    $('#slide-container').owlCarousel({
        'singleItem': true,
        'autoPlay': 5000,
        'autoHeight': true,
        'stopOnHover': true,
        'theme': "big-marquee",
    });
    $('#resources-carousel').owlCarousel({
        'items': 3,
        'pagination': false,
        'stopOnHover': true,
        'theme': 'resource-theme',
    });
    if($('.nav-mobile').is(':visible')) {
        $('#history-carousel').owlCarousel(history_mobile);  
    } else {
        $('#history-carousel').owlCarousel(history_not_mobile);  
    }
    $('#member-professionals-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 5000,
        'pagination': false,
        'stopOnHover': true,
        'theme': 'members-theme',
    });
    $('#member-organization-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 5000,
        'pagination': false,
        'stopOnHover': true,
        'theme': 'members-theme',
    }).hide()
        .data('owlCarousel').stop();
    $('#hcal-professionals-carousel').owlCarousel({
        'singleItem': true,
        'pagination': true,
        'theme': "normal-marquee",   
    });
    $('#hcal-families-carousel').owlCarousel({
        'singleItem': true,
        'pagination': true,
        'theme': "normal-marquee",
    });
    $(window).resize(function(e) {
        if($('.nav-mobile').is(':visible')) {
            $('#history-carousel').data('owlCarousel').reinit(history_mobile);  
        } else {
            $('#history-carousel').data('owlCarousel').reinit(history_not_mobile);  
        }
        return true;
    });
});
$('#home-resources').on('click', 'a[class^="button"]', function() {
    if($(this).hasClass('button-prev')) {
        $('#resources-carousel').trigger('owl.prev');
    } else {
        $('#resources-carousel').trigger('owl.next');
    }
});
$('#home-history').on('click', 'a[class^="button"]', function() {
    if($(this).hasClass('button-prev')) {
        slideImage($('#history-carousel'), 'prev');
    } else {
        slideImage($('#history-carousel'), 'next');
    }
});
$('.training-button').on('click', function(e) {
    e.preventDefault();
    if($(this).attr('id') === 'training-families') {
        $('.hcal-right-side .selected').removeClass('selected');
        $(this).addClass('selected');
        $('#hcal-families').show();
        $('#hcal-professionals').hide();
    } else {
        $('.hcal-right-side .selected').removeClass('selected');
        $(this).addClass('selected');
        $('#hcal-families').hide();
        $('#hcal-professionals').show();
    }
});

$('.member-button').on('click', function() {
    if($(this).attr('id') === 'member-professionals') {
        $('.member-active').removeClass('member-active');
        $(this).addClass('training-active');
        $('#member-professionals-carousel').show()
            .data('owlCarousel').play();
        $('#member-organization-carousel').hide()
            .data('owlCarousel').stop();
    } else {
        $('.member-active').removeClass('member-active');
        $(this).addClass('training-active');
        $('#member-organization-carousel').show()
            .data('owlCarousel').play();
        $('#member-professionals-carousel').hide()
            .data('owlCarousel').stop();
    }
});

function slideImage(elem, direction) {
    elem.find('.active .history-image').slideToggle(500, function() {
        elem.trigger('owl.'+direction);
    });
}