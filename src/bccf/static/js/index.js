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
    'slideSpeed': 2000,
    'paginationSpeed': 2000,
    'rewindSpeed': 4000,
    'pagination': false,
    'stopOnHover': true,
    'addClassActive': true,
    'autoPlay': false,
    'responsiveRefreshRate': 1,
    'afterMove': function(elem) { slideUpImage(elem); },
    'afterUpdate': function(elem) { prep_history_carousel(elem); },
    'afterInit': function(elem) { elem.find('.active .history-image').show(); },
    'theme': 'history-theme',
};
var history_mobile = {
    'singleItem': true,
    'pagination': false,
    'autoPlay': true,
    'afterMove': false,
    'responsiveRefreshRate': 1,
    'afterInit': function(elem) { elem.find('.history-image').show(); },
    'afterUpdate': function(elem) { prep_history_carousel(elem); },
};
$(function(){
    $('#slide-container').owlCarousel({
        'singleItem': true,
        'autoPlay': 10000,
	    'slideSpeed': 2000,
	    'paginationSpeed': 2000,
	    'rewindSpeed': 4000,
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
        'addClassActive': true,
        'theme': 'normal-marquee',
        'beforeMove': function(elem) {
            if(!elem.is(':hover') && (this.owl.currentItem+1) === this.owl.owlItems.length && !$('.mnav-mobile-btn').is(':visible')) {
                $('#member-organization').trigger('click');
            }
        }
    });
    $('#member-organization-carousel').owlCarousel({
        'singleItem': true,
        'autoPlay': 5000,
        'pagination': true,
        'stopOnHover': true,
        'theme': 'normal-marquee',
        'addClassActive': true,
        'beforeMove': function(elem) {
            if(!elem.is(':hover') && (this.owl.currentItem+1) === this.owl.owlItems.length && !$('.mnav-mobile-btn').is(':visible')) {
                $('#member-professionals').trigger('click');
            }
         }
    });
    $('#hcal-professionals-carousel').owlCarousel({
        'singleItem': true,
        'pagination': true,
        'autoPlay': 7000,
        'stopOnHover': true,
        'theme': "normal-marquee",
        'beforeMove': function(elem) {
            if(!elem.is(':hover') && (this.owl.currentItem+1) === this.owl.owlItems.length && !$('.mnav-mobile-btn').is(':visible')) {
                $('#training-families').trigger('click');
            }
        }
    });
    $('#hcal-families-carousel').owlCarousel({
        'singleItem': true,
        'pagination': true,
        'autoPlay': 7000,
        'stopOnHover': true,
        'theme': "normal-marquee",
        'beforeMove': function(elem) {
            if(!elem.is(':hover') && (this.owl.currentItem+1) === this.owl.owlItems.length && !$('.mnav-mobile-btn').is(':visible')) {
                $('#training-professionals').trigger('click');
            }
        }
    });
    $('#training-families').trigger('click');
    $('#member-organization').trigger('click');
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
    var owl = null;
    var not_owl = null;
    $('.training-button.selected').removeClass('selected');
    $(this).addClass('selected');
    if($(this).attr('id') === 'training-families') {
        owl = $('#hcal-families-carousel');
        not_owl = $('#hcal-professionals-carousel');
    } else {
        owl = $('#hcal-professionals-carousel');
        not_owl = $('#hcal-families-carousel');
    }
    not_owl.hide();
    not_owl.data('owlCarousel').stop();
    owl.show();
    owl.data('owlCarousel').play();
});

$('.member-button').on('click', function(e) {
    e.preventDefault();
    var owl = null;
    var not_owl = null;
    $('.member-button.selected').removeClass('selected');
    $(this).addClass('selected');
    if($(this).attr('id') === 'member-professionals') {
        owl = $('#member-professionals-carousel');
        not_owl = $('#member-organization-carousel');
    } else {
        owl = $('#member-organization-carousel');
        not_owl = $('#member-professionals-carousel');
    }
    if(owl.find('.owl-item').length > 1) {
        owl.data('owlCarousel').jumpTo(0);
    }
    not_owl.hide();
    not_owl.data('owlCarousel').stop();
    owl.show();
    owl.data('owlCarousel').play();
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
