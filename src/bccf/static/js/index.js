var prep_history_carousel = function(elem) {
    history_height = elem.find('.history-image:first-child').height();
    elem.find('.history-image:first-child').css({top:0});
    if($('.mnav-mobile-btn').is(':visible')) {
        elem.data('owlCarousel').reinit(history_mobile);
    } else {
        elem.data('owlCarousel').reinit(history_not_mobile);
        elem.data('owlCarousel').stop();
    }
};
var history_not_mobile = {
    'singleItem': true,
    'slideSpeed': 800,
    'paginationSpeed': 800,
    'rewindSpeed': 800,
    'pagination': false,
    'stopOnHover': true,
    'addClassActive': true,
    'autoPlay': false,
    'responsiveRefreshRate': 1,
    'afterMove': function(elem) { slideUpImage(elem); },
    'afterUpdate': function(elem) { prep_history_carousel(elem); },
    'afterInit': function(elem) { elem.find('.active .history-image').show(); },
    'theme': 'history-theme',
}
var history_mobile = {
    'singleItem': true,
    'pagination': false,
    'autoPlay': true,
    'afterMove': false,
    'responsiveRefreshRate': 1,
    'afterInit': function(elem) { elem.find('.history-image').show(); },
    'afterUpdate': function(elem) { prep_history_carousel(elem); },
}
$(function(){
    $('#slide-container').owlCarousel({
        'singleItem': true,
        'autoPlay': true,
        'stopOnHover': true,
        'theme': "big-marquee",
    });
    $('#programs-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 20000,
        'stopOnHover': true,
        'theme': "med-marquee",
        'autoHeight': true,
    });
    $('#noteworthy-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 15000,
        'stopOnHover': true,
        'theme': "med-marquee",
        'autoHeight': true,
    });
    $('#carousel-resources').owlCarousel({
        'items': 3,
        'pagination': false,
        'addClassActive': true,
        'itemsDesktop': false,
        'itemsDesktopSmall': [1120, 2],
        'itemsMobile': [600, 1],
    });
    if($('.mnav-mobile-btn').is(':visible')) {
        $('#history-carousel').owlCarousel(history_mobile);
    } else {
        $('#history-carousel').owlCarousel(history_not_mobile);  
    }
    $('#member-professionals-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 5000,
        'pagination': true,
        'stopOnHover': true,
        'theme': 'normal-marquee',
    });
    $('#member-organization-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 5000,
        'pagination': true,
        'stopOnHover': true,
        'theme': 'normal-marquee',
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
});
$('#home-resources').on('click', 'a[class^="button"]', function() {
    if($(this).hasClass('button-prev')) {
        $('#carousel-resources').trigger('owl.prev');
    } else {
        $('#carousel-resources').trigger('owl.next');
    }
});
$('#home-history').on('click', 'a[class^="button"]', function() {
    if($(this).hasClass('button-prev')) {
        slideDownImage($('#history-carousel'), 'prev');
    } else {
        slideDownImage($('#history-carousel'), 'next');
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

$('.member-button').on('click', function(e) {
    e.preventDefault();
    $('#home-listings .selected').removeClass('selected');
    $(this).addClass('selected');
    if($(this).attr('id') === 'member-professionals') {
        $('#member-professionals-carousel').show()
            .data('owlCarousel').play();
        $('#member-organization-carousel').hide()
            .data('owlCarousel').stop();
    } else {
        $('#member-organization-carousel').show()
            .data('owlCarousel').play();
        $('#member-professionals-carousel').hide()
            .data('owlCarousel').stop();
    }
});

function slideDownImage(elem, direction) {
    elem.find('.active .history-image').css({position:'relative'})
    .animate({
        top: -20,
    }, {
        duration: 100,
        step: function(now, fx) {
            if (fx.prop == "top") {
                $(fx.elem).scroll(now);
            }
        },
    })
    .delay(100)
    .animate({
        top: $(this).height()
    }, {
        duration: 200,
        step: function(now, fx) {
            if (fx.prop == "top") {
                $(fx.elem).scroll(now);
            }
        },
        complete: function() {
            elem.trigger('owl.'+direction);    
        }  
    });
}

function slideUpImage(elem) {
    elem.find('.history-image').hide();
    var $revealMe = elem.find('.active .history-image');
    $revealMe.css({
        position: "relative",
        top: $(this).height(),           
    }).delay(800).show().animate({
        top: -20,
    }, {
        duration: 200,
        step: function(now, fx) {
            if (fx.prop == "top") {
                $(fx.elem).scrollTop(now);
            }
        }
    }).delay(20).animate({
        top: 0,        
    }, {
        duration: 20,
        step: function(now, fx) {
            if (fx.prop == "top") {
                $(fx.elem).scroll(now);
            }
        }
    });    
}