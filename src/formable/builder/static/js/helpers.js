// Fields that will be created when the name is dropped
var fields = {
    'text-field': '<label for="text-field">Text</label>: <input type="text" name="text-field"/>',
    'textarea-field': '<label for="textarea-field">Multiline</label>: <textarea name="textarea-field" rows="4" cols="5"></textarea>',
    'password-field': '<label for="password-field">Password</label>: <input type="password" name="password-field"/>',
    'select-field': '<label for="select-field">Select</label>: <select name="select-field"><option>Option 1</option><option>Option 2</option><option>Option 3</option></select>',
    'multiselect-field': '<label for="multiselect-field">Multiselect</label>: <select multiple name="multiselect-field"><option>Option 1</option><option>Option 2</option><option>Option 3</option></select>',
    'checkbox-field': '<label for="checkbox-field">Checkbox</label>: <div class="buttons inline"><input type="checkbox" name="checkbox-field"/><span>Checkbox 1</span><input type="checkbox" name="checkbox-field"/><span>Checkbox 2</span><input type="checkbox" name="checkbox-field"/><span>Checkbox 3</span></div>',
    'radioset-field': '<label for="radioset-field">Radioset</label>: <div class="buttons inline"><input type="radio" name="radioset-field"/><span>Radio 1</span><input type="radio" name="radioset-field"/><span>Radio 2</span><input type="radio" name="radioset-field"/><span>Radio 3</span></div>',
    'static-text-field': '<span>Static Text Field</span>',
    'static-section-field': '<span class="section-head">Section Heading</span>',
};

/*
 * edit_field
 *
 * Edits a field in a fieldset.
 *
 * Parameters:
 * obj - the row containing the field to be edited
 * 
 * Notes:
 * Must be used only with fields.
 */
var edit_field = function(obj) {
    var settings = $("#settings-box");
    var title = "";
    var form = "";
    var update = function(){};
    
    obj.addClass('row-active');
    
    // Giant if else statement for each type of field!
    if(obj.hasClass('static-text-field') || obj.hasClass('static-section-field')) { // Static Text
        title += 'Editing: '+obj.children('span').html();
        form += get_text_field('Text', obj.children('span').html(), 'text');
        update = function() {
            obj.children('span').html($("#text").val());
        };
    } else if(obj.hasClass('text-field') || obj.hasClass('password-field')) { // Text Fields
        title += 'Editing: '+obj.children('label').html();
        form += get_text_field('Label', obj.children('label').html(), 'label');
        form += get_text_field('Name', obj.children('input').attr('name'), 'name');
        if(!obj.hasClass('password-field')) {
            form += get_text_field('Placeholder', obj.children('input').attr('placeholder'), 'placeholder');
        }
        form += get_check_field('Required', obj.children('input').attr('required') !== 'required' ? '' : 'checked', 'required');
        update = function() {
            obj.children('label').html($("#label").val());
            obj.children('input').attr('name', $("#name").val());
            if($("#placeholder").val() !== '') {
                obj.children('input').attr('placeholder', $("#placeholder").val());
            } else {
                obj.children('input').removeAttr('placeholder');
            }
            if($('#required').is(':checked')) {
                console.log('checked');
                obj.children('input').attr('required', '');
            } else {
                obj.children('input').removeAttr('required');
            }
        };
    } else if(obj.hasClass('textarea-field')) {
        title += 'Editing: '+obj.children('label').html();
        form += get_text_field('Label', obj.children('label').html(), 'label');
        form += get_text_field('Name', obj.children('textarea').attr('name'), 'name');
        form += get_text_field('Columns', obj.children('textarea').attr('cols'), 'cols');
        form += get_text_field('Rows', obj.children('textarea').attr('rows'), 'rows');
        form += get_check_field('Required', obj.children('textarea').attr('required') !== 'required' ? '' : 'checked', 'required');
        update = function() {
            obj.children('label').html($("#label").val());
            obj.children('textarea').attr('name', $("#name").val());
            obj.children('textarea').attr('cols', $("#cols").val());
            obj.children('textarea').attr('rows', $("#rows").val());
            if($('#required').is(':checked')) {
                obj.children('textarea').attr('required', '');
            } else {
                obj.children('textarea').removeAttr('required');
            }
        }
    } else if(obj.hasClass('select-field') || obj.hasClass('multiselect-field')) {
        var options = '';
        $.each(obj.children('select').children('option'), function() {
            options += $(this).html()+'\n';
        });
        title += 'Editing: '+obj.children('label').html();
        form += get_text_field('Label', obj.children('label').html(), 'label');
        form += get_text_field('Name', obj.children('select').attr('name'), 'name');
        form += get_textarea_field('Options', options, 'options');
        form += get_check_field('Required', obj.children('select').attr('required') !== 'required' ? '' : 'checked', 'required');
        update = function() {
            var newoptions = '';
            obj.children('label').html($("#label").val());
            obj.children('select').attr('name', $("#name").val())
            $.each($("#options").val().split('\n'), function(index, value) {
                if(value !== '') {
                    newoptions += '<option>'+value+'</option>';
                }
            });
            obj.children('select').html(newoptions);
            if($('#required').is(':checked')) {
                obj.children('select').attr('required', '');
            } else {
                obj.children('select').removeAttr('required');
            }
        }
    } else if(obj.hasClass('radioset-field') || obj.hasClass('checkbox-field')) {
        var buttons = '';
        var type = obj.hasClass('radioset-field') ? 'radio' : 'checkbox';
        $.each(obj.find('input'), function() {
            buttons += $(this).next().html()+'\n';
        });
        title += 'Editing: '+obj.children('label').html();
        form += get_text_field('Label', obj.children('label').html(), 'label');
        form += get_text_field('Name', obj.find('input').attr('name'), 'name');
        form += get_textarea_field('Buttons', buttons, 'buttons');
        update = function() {
            var newbuttons = '';
            $.each($("#buttons").val().split('\n'), function(index, value) {
                if(value !== '') {
                    newbuttons += '<input type="'+type+'" name="'+$("#name").val()+
                    '" value="'+value+'"/><span>'+value+'</span>';
                }
            });
            obj.children('label').html($("#label").val());
            obj.children('.buttons').html(newbuttons);
        };
    } else {
        console.log('Field does not exist');
        obj.removeClass('row-active');
        return;
    }
    
    settings.children("#settings-title").html(title);
    settings.children("table").html(form);
    
    // Generic dialog box
    settings.dialog({
        height: 'auto',
        width: 500,
        modal: true,
        buttons: {
            'Update': function() {
                update();
                obj.removeClass('row-active');
                settings.dialog("close");
            },
            Cancel: function() {
                obj.removeClass('row-active');
                $(this).dialog("close");
            }
        },
        Close: function () {
            console.log('close');
            obj.removeClass('row-active');
            $(this).dialog("close");
        }
    });
    settings.dialog("open");
}

/*
 * edit_row
 *
 * Edits the name of the fieldset or row
 *
 * Parameters:
 * obj - the fieldset obj to be edited
 *
 * Notes:
 * To be used only for fieldsets or rows
 */
var edit_row = function(obj) {    
    $("#settings-box").children("table").html(get_text_field('Fieldset Name', obj.html(), 'name'));
    $("#settings-box").children('#settings-title').html('Editig Fieldset: '+obj.html());
    $("#settings-box").dialog({
        height: 'auto',
        width: 500,
        modal: true,
        buttons: {
            'Update': function() {
                obj.html($("#name").val());
                $(this).dialog("close");
            },
            Cancel: function() {
                $(this).dialog("close");
            }
        },
    });
    $("#settings-box").dialog("open");
}

/*
 * add_row
 *
 * Creates a new row or fieldset.
 *
 * Notes:
 * Opens up a modal box asking the user what to name the fieldset. The fieldset
 * can be empty.
 */
var add_row = function() {
    $("#settings-box").children("table").html(get_text_field('Fieldset Name', '', 'name'));
    $("#settings-box").children('#settings-title').html('Add Fieldset');
    $("#settings-box").dialog({
        height: 'auto',
        width: 500,
        modal: true,
        buttons: {
            'Add': function() {
                $("#form-body").append(create_fieldset("#form-body", $("#name").val()));
                $(this).dialog("close");
            },
            Cancel: function() {
                $(this).dialog("close");
            }
        },
    });
    $("#settings-box").dialog("open");
}

/*
 * export_form
 *
 * Exports the form into a JSON string.
 */
var export_form = function() {
    var fieldsetCounter = 0;
    var start = $("#form-body");
    var obj = new Object();
    obj.title = $("#form-title").val();
    obj.fieldset = []
    
    $.each($("#form-body").children("li"), function() {
        var fieldset = new Object();
        fieldset.title = $(this).children("fieldset").children("legend").html();
        fieldset.fields = [];
        
        $.each($(this).children("fieldset").find("ul li"), function() {
            var field = new Object();
            var classes = $(this).attr("class").split(/\s/);
            field.class = classes[0];
            field.label = $(this).children("label").html();
            field.attr = new Object();
        
            if($(this).hasClass("static-text-field") || $(this).hasClass("static-section-field")) {
                field.attr.type = $(this).hasClass("static-text-field") ? "static-text" : "static-section";
                field.attr.text = $(this).children("span").html();
            } else if($(this).hasClass("text-field") || $(this).hasClass("password-field")) {
                field.attr.type = $(this).children("input").attr("type");
                field.attr.name = $(this).children("input").attr("name");
                field.attr.placeholder = $(this).children("input").attr("placeholder");
                field.attr.required = $(this).children("input").attr("required");
            } else if($(this).hasClass("textarea-field")) {
                field.attr.type = "textarea"
                field.attr.name = $(this).children("textarea").attr("name");
                field.attr.cols = $(this).children("textarea").attr("cols");
                field.attr.rows = $(this).children("textarea").attr("rows");
                field.attr.required = $(this).children("textarea").attr("required");
            } else if($(this).hasClass("select-field") || $(this).hasClass("multiselect-field")) {
                field.options = [];
                field.attr.name = $(this).children("select").attr("name");
                field.attr.type = "select";
                field.attr.multiple = $(this).children("select").attr("multiple");
                $.each($(this).children("select").children("option"), function() {
                    field.options.push($(this).html());
                });
            } else if($(this).hasClass("checkbox-field") || $(this).hasClass("radioset-field")) {
                field.options = [];
                field.attr.name = $(this).find("input").attr("name");
                field.attr.type = $(this).hasClass("checkbox-field") ? "checkbox" : "radio";
                $.each($(this).find("input"), function() {
                    field.options.push($(this).next().html());
                });
            }
            
            fieldset.fields.push(field);
        });
        
        obj.fieldset.push(fieldset);
    });
    
    $("#form_structure_title").val(obj.title);
    $("#form_structure_data").val(JSON.stringify(obj));
    $("#form_structure_type").val('JSON');
    $("#form_structure_form").submit();
}

/*
 * import_form
 *
 * Creates a form based off of a JSON string
 */
var import_form = function(json) {
    var obj = $.parseJSON(json);
    var formbody = $("#form-body");
    formbody.html("");
    
    if(obj === null) {
        obj = json
    }
    
    $("#form-title").val(obj.title);
    
    $(obj).each(function(i, form) {
        $(form.fieldset).each(function(i, fieldset) {
            create_fieldset("#form-body", fieldset.title);
            $(fieldset.fields).each(function(i, field) {
                var lastli = create_field($("#form-body").children("li:last-child"), field.class);
                
                if(field.class === 'static-text-field' || field.class === 'static-section-field') {
                    lastli.children('span').html(field.attr.text);
                } else if(field.class === "text-field" || field.class === "password-field") {
                    console.log(lastli.children('label'));
                    lastli.children('label').html(field.label);
                    lastli.children('input').attr('name', field.attr.name);
                    if(field.attr.placeholder !== 'undefined') {
                        lastli.children('input').attr('placeholder', field.attr.placeholder);
                    }
                    if(field.attr.required !== 'undefined') {
                        lastli.children('input').attr('required', '');
                    }
                } else if(field.class === 'textarea-field') {
                    lastli.children('label').html(field.label);
                    lastli.children('textarea').attr('name', field.attr.name);
                    lastli.children('textarea').attr('cols', field.attr.cols);
                    lastli.children('textarea').attr('rows', field.attr.rows);
                    if(field.required !== 'undefined') {
                        lastli.children('textarea').attr('required', '');
                    }
                } else if(field.class === 'select-field' || field.class === 'multiselect-field') {
                    lastli.children('label').html(field.label);
                    lastli.children('select').attr('name', field.attr.name);
                    if(field.attr.multiple === 'multiple') {
                        lastli.children('select').attr('multiple', '');
                    }
                    var newoptions = '';
                    $(field.options).each(function(i, options) {
                        newoptions += '<option>'+options+'</option>';
                    });
                    lastli.children('select').html(newoptions);
                    if(field.attr.required !== 'undefined') {
                        lastli.children('textarea').attr('required', '');
                    }
                } else if(field.class === 'checkbox-field' || field.class === 'radioset-field') {
                    lastli.children('label').html(field.label);
                    var newbuttons = ''
                    $(field.options).each(function(i, button) {
                        newbuttons += '<input type="'+field.attr.type+'" name="'+field.attr.name+
                            '" value="'+button+'"/><span>'+button+'</span>';
                    });
                    lastli.children('.buttons').html(newbuttons);
                }
            });  
        });
    });
}

// Field Edit Helpers

/*
 * del_row
 *
 * Deletes a field row or a fieldset from the form body.
 *
 * Parameters:
 * obj - the row (jQuery object) object that will be deleted.
 *
 * Notes:
 * This is best used as removing a 'li' group from a 'ul' group.
 */
var del_row = function(obj) {
    obj.remove();
}

/*
 * get_text_field
 *
 * Creates an empty input text form field.
 *
 * Parameters:
 * label - label of for the input text
 * val - current value of the input text
 * id - id of the input name but will be as the name as well
 *
 * Notes:
 * Wraps the input field in a table row, change the wrapper as necessary.
 */
var get_text_field = function(label, val, id) {
    val = typeof val !== 'undefined' ? val : '';
    
    return '<tr><th><label for="'+id+'">'+label+'</label>:</th><td><input name="'+id+'" id="'
        +id+'" type="text" value="'+val+'"/></td></tr>';   
}

/*
 * get_check_field
 *
 * Creates an empty checkbox field.
 *
 * Parameters:
 * label - label for the checkbox
 * checked - checked or undefined
 * id - id of the input name but will be as the name as well
 *
 * Notes:
 * Wraps the input field in a table row, change the wrapper as necessary
 */
var get_check_field = function(label, checked, id) {
    checked = typeof checked !== 'undefined' ? checked : '';
    
    return '<tr><th><label for="'+id+'">'+label+'</label>:</th><td><input name="'+id+'" id="'
        +id+'" type="checkbox" '+checked+'/></td></tr>';
}

/*
 * get_textarea_field
 *
 * Creates an empty input text form field.
 *
 * Parameters:
 * label - label of for the input text
 * val - current value of the input text
 * id - id of the input name but will be as the name as well
 *
 * Notes:
 * Wraps the input field in a table row, change the wrapper as necessary.
 */
var get_textarea_field = function(label, val, id) {
    val = typeof val !== 'undefined' ? val : '';
    
    return '<tr><th><label for="'+id+'">'+label+'</label>:</th><td><textarea name="'+id+'" \
    id="'+id+'" rows="10">'+val+'</textarea>';
}

var create_fieldset = function(id, legend) {
    $(id).append(   
        '<li class="form_row row draggable droppable"><fieldset class="container"><legend>'
        +legend+'</legend><ul class="ten col no-style-list sortable"></ul>\
        <div class="icon-container two">\
            <b class="sort-icon"></b>\
            <b class="del-icon"></b>\
            <b class="edit-icon"></b>\
        </div></fieldset></li>'
    );
        
    var lastli = $(id+" li:last-child");
    var icons = lastli.children("fieldset").children(".icon-container");
    
    lastli.droppable({
        accept: ".field",
        hoverClass: "row-active",
        drop: function(event, ui) {
            create_field(lastli, ui.draggable.attr('id'));
        },
    })
    .find('ul').sortable();
    icons.children(".del-icon").on('click', function(){del_row(lastli)});
    icons.children(".edit-icon").on('click', function(){edit_row(lastli.find("legend"))});
}

var create_field = function(lastli, id) {
    var fieldul = lastli.children('fieldset').children('ul');
    
    fieldul.append('<li class="'+id+' row-one twelve">'
        +fields[id]+'<div class="icon-container three">\
            <b class="sort-icon"></b>\
            <b class="del-icon"></b>\
            <b class="edit-icon"></b>\
        </div></fieldset></li>');
    
    var fieldlastli = fieldul.children("li:last-child");
    var fieldicons = fieldlastli.find(".icon-container");
    fieldicons.children(".del-icon").on('click', function(){del_row(fieldlastli)});
    fieldicons.children(".edit-icon").on('click', function(){edit_field(fieldlastli)});
    
    return fieldlastli;
}
