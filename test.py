"""
what do I need to form a report file?
I need the following:
1- Columns names
2- Data for each column

what should I offer the user in order to make him/her capable of
using this functionality in a relived way:
1- offer him/her the availability of choosing columns names
2- offer him/her the availability of choosing pages

create a function that takes the following arguments as inputs:
- actual model class
- selected pages
- selected headers
- paginator object

* notes to consider:
- header array contains columns' names in the html page

"""
def get_column_names_from_queryset(queryset):
    # for word in queryset:
    pass
def prepare_selected_query(model,headers,selected_pages,paginator_object):
    # model._meta.fields
    # define construct object
    constructor = {}
    # loop through headers
    for header in headers:
        # loop through fields names of the model
        # check for the existing of each column in the headers array
        for field_name in model._meta.fields:
            if header == field_name:
                # loop through selected pages
                # define temporary array
                temp_array = []
                for page in selected_pages:
                    # loop through objects in the page
                    for object in paginator_object.page(page):
                        # add field value to the temporary array
                        temp_array.append(getattr(object,field_name))
                # add the array to the constructor
                constructor.update({field_name: temp_array})

def convert_field_name_to_readable_name(field_name):
    words_in_field_name = ""
    for word in field_name.split("_"):
        words_in_field_name += word.capitalize()+" "
    print( words_in_field_name)

def convert_header_names_to_readable_names(headers):
    converted_names = []
    for sentence in headers:
        result_word = ""
        for word in sentence.split("_"):
            result_word+=word.capitalize() + " "
        converted_names.append(result_word.strip(" "))
    return converted_names




if __name__ == "__main__":
    print(convert_header_names_to_readable_names(["full_name","gender_name","name"]))