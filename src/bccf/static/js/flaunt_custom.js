(function($, window) {
    var Flaunt = {
        init: function(options, elem) {
            var base = this;
            base.$elem = $(elem);
            base.options = $.extend({}, $.fn.Flaunt.options, base.$elem.data(), options);
            base.prepContainer();
            base.buildWidget();
        },
        buildWidget: function() {
            var base = this;
            if(base.options.mobileContainer === null) {
                var mobileContainer = $('<div/>', {
                    class: "nav-mobile"
                });
            } else {
                var mobileContainer = $(base.options.mobileContainer);
                mobileContainer.addClass('nav-mobile');
            }
            base.$elem.append(mobileContainer);
            base.$elem.children('.nav-list').children('.nav-item').has('ul').prepend('<span class="nav-click"><i class="nav-arrow"></i></span>');                        
            mobileContainer.on('click', function() {
                base.$elem.children('.nav-list').slideToggle(200);        
            });
            base.$elem.children('.nav-list').on('click', '.nav-click', function() {
                $(this).siblings('.nav-submenu').toggle();
                $(this).children('.nav-arrow').toggleClass('nav-rotate');
            });
            $(window).resize(function() {
                if(!mobileContainer.is(':visible') && !base.$elem.children('.nav-list').is(':visible')) {
                    console.log('resize');
                    base.$elem.children('.nav-list').show(); 
                } else if(mobileContainer.is(':visible') && base.$elem.children('.nav-list').is(':visible')) {
                    base.$elem.children('.nav-list').hide();     
                }
            });
        },
        prepContainer: function() {
            var base = this; 
            base.$elem.children('ul').addClass('nav-list');
            base.$elem.children('.nav-list').children('li').addClass('nav-item');
            base.$elem.children('.nav-list').children('li').children('ul').addClass('nav-submenu');
            base.$elem.children('.nav-list').children('li').children('ul').children('li').addClass('nav-submenu-item');    
        },
    };
    $.fn.Flaunt = function(options) {
        return this.each(function() {
          var flaunt = Object.create(Flaunt);
          flaunt.init(options, this);
          $.data(this, 'Flaunt', flaunt);
        });
    };
    $.fn.Flaunt.options = {
        mobileContainer: null   // Id of the DIV that will contain the mobile button
    };
})(jQuery, window);