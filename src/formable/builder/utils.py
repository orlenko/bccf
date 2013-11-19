import collections
import json
import re

from django import forms

from formable.builder.models import Question
from formable.builder.fields import StaticTextField, StaticText, StaticSection

def parse(struct, publish_id):
    """
    Parses the struct and uses BetterForm to create the form with the specified
    fields in fieldsets.
    """
    fieldsets = []
    fields = {} 
    form_struct = convert(json.loads(struct))
    
    for fieldset in form_struct["fieldset"]: # Each fieldset
        new_set = {}
        new_set["legend"] = fieldset["title"]
        new_set["fields"] = []
        for field in fieldset["fields"]: # Each field in the fieldset
            isRequired = False
            if "required" in field["attr"]: # Check if the field is required
                isRequired = True
                
            # Create new field for each field
            
            # Text, Password, Textarea
            if field["class"] == "text-field" or field["class"] == "password-field" or field["class"] == "textarea-field":
                if field["class"] == "text-field":
                    field_class = forms.CharField(label=field["label"],
                        required=isRequired,
                        widget=forms.TextInput(field["attr"]))
                elif field["class"] == "password-field":
                    field_class = forms.CharField(label=field["label"],
                        required=isRequired,
                        widget=forms.PasswordInput(field["attr"]))
                else:
                    field_class = forms.CharField(label=field["label"],
                        required=isRequired,
                        widget=forms.Textarea(field["attr"]))
                        
            # Select, Radioset
            elif field["class"] == "select-field" or field["class"] == "radioset-field":
                if field["class"] == "select-field":
                    field_class = forms.ChoiceField(label=field["label"],
                        required=isRequired,
                        choices=create_choices(field["options"]))
                else:
                    field_class = forms.ChoiceField(label=field["label"],
                        required=isRequired,
                        widget=forms.RadioSelect,
                        choices=create_choices(field["options"]))
            
            # MultiSelect, Checkboxes
            elif field["class"] == "multiselect-field" or field["class"] == "checkbox-field":
                if field["class"] == "multiselect-field":
                    field_class = forms.MultipleChoiceField(label=field["label"],
                        required=isRequired,
                        choices=create_choices(field["options"]))
                else:
                    field_class = forms.MultipleChoiceField(label=field["label"],
                        required=isRequired,
                        widget=forms.CheckboxSelectMultiple,
                        choices=create_choices(field["options"]))
                        
            # StaticText, StaticSection
            elif field["class"] == "static-text-field" or field["class"] == "static-section-field":
                if field["class"] == "static-text-field":
                    field_class = StaticTextField(label="", widget=StaticText(value=field["attr"]["text"]))
                else:
                    field_class = StaticTextField(label="", widget=StaticSection(value=field["attr"]["text"]))

            if field["class"] == "static-text-field" or field["class"] == "static-section-field":
                fields[re.sub(r"[-\s]", "_", field["attr"]["text"].lower())] = field_class
                new_set["fields"].append(re.sub(r"[-\s]", "_", field["attr"]["text"].lower()))
            else:
                question = Question.objects.get(form_published=publish_id, question__exact=field["label"])
                fields[str(question.id)+"."+re.sub(r"[-\s]", "_", field["class"]).lower()] = field_class
                new_set["fields"].append(str(question.id)+"."+re.sub(r"[-\s]", "_", field["class"]).lower())
            # end for field
        
        # Add fieldset to the fieldset list
        fieldsets.append((re.sub(r"[-\s]", "_", fieldset["title"].lower()),) + (new_set,)) # Add new fieldset to the list
        # end for fieldset
    return fieldsets, fields
  
def create_choices(lst):
    """
    Creates the proper structure for the django form choices.
    """
    to_tuple = []
    for choice in lst:
        tmp = (choice,) + (choice,)
        to_tuple.append(tmp)
    return tuple(to_tuple)
    
def convert(data):
    """
    Converts everything in a dictionary from unicode to string
    """
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
