/**
 * This whole file is a filthy hack to make django-ckeditor work with Grappelli's
 * inlines.
 *
 * Inlines can be dynamically added at any time, and we need to run CKEDITOR.replace
 * on their fields once they're added.
 *
 * But we do NOT run it on the "template" inline, of course.
 *
 * Oh, and there's no way to register a "callback" for Grappelli to call when it adds
 * a new inline without overriding the entire change form, which this tiny app does
 * not want to do.
 *
 * Basically: this file runs a function every second that checks for new
 * .django-ckeditor fields, and will convert them to CKEditors if it finds any.
 *
 * TODO: Handle removal of inlines too.
 * TODO: Experiment with frequencies to find a good combination of responsiveness and CPU-eating.
 */

if (!window.Django_CKEditor_Configs) {
	window.Django_CKEditor_Configs = [];
}

$(function() {
    var done = [];

    var InitCKEditors = function() {
    	var jq = $ || django.jQuery;
        jq('.django-ckeditor').each(function(i, el) {
            var elid = jq(el).attr('id');

            // Don't mess with the "template" versions.
            if (elid.indexOf('__prefix__') == -1) {
                if (jq.inArray(elid, done) == -1) {
                    var config = null;

                    // Find the config that applies to this CKEditor.
                    jq.each(window.Django_CKEditor_Configs, function(i, val) {
                        if (val.re.test(elid)) {
                            config = val.config;
                            return false;
                        }
                    });

                    CKEDITOR.replace(elid, config);
                    done.push(elid);
                }
            }
        });

        setTimeout(InitCKEditors, 1000);
    };

    setTimeout(InitCKEditors, 100);
})
