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
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter


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
def create_report():
    import os
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY,fontName="Courier",fontSize=12))
    import datetime
    today = datetime.date.today()
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    path = str(Path(__file__).resolve().parent)+"/apps" + str("/OrdersReports")
    file_name = 'order_details_'+str(today)+ ".pdf"
    complete_file_path = os.path.abspath(path) + "/" + file_name
    user_details_headers = ["Full Username","Phone Number","Email"]
    user_details = ["Mohammed Ali Abbas","0999627379","hysoca7@gmail.com"]
    order_details_headers = ["Product Name","Product Price","Quantity","Total"]
    order_data = []
    order_data.append(order_details_headers)
    first_order_details = ["A product",230,1,230]
    second_order_details = ["B product",100,2,200]
    third_order_details = ["C product",900,2,1800]
    order_data.append(first_order_details)
    order_data.append(second_order_details)
    order_data.append(third_order_details)
    pdf = SimpleDocTemplate(
        complete_file_path,
        pagesize=letter,
        title="Order Details",
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18,

    )

    user_data = [
        user_details_headers,
        user_details
    ]
    order_table = Table(order_data)
    user_table = Table(user_data)
    # add style
    style = TableStyle([
        ("BACKGROUND",(0,0),(3,0),colors.cornflowerblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
        ("ALIGN",(0,0),(-1,-1),'CENTER'),
        ("FONTNAME",(0,0),(-1,0),'Courier'),
        ("FONTSIZE",(0,0),(-1,0) ,12),
        ("BOTTOMPADDING",(0,0),(-1,0) ,12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("BOX", (0, 0), (-1, -1),1, colors.black),

    ])
    order_table.setStyle(style)
    user_table.setStyle(style)
    elems = []
    elems.append(Paragraph("Order Details", styles["Justify"]))
    elems.append(Spacer(1, 20))
    elems.append(order_table)
    elems.append(Spacer(1,40))
    elems.append(Paragraph("User Details", styles["Justify"]))
    elems.append(Spacer(1, 20))
    elems.append(user_table)
    elems.append(Spacer(1,40))
    elems.append(Paragraph(f'Report Date and Time {today} -- {current_time} ', styles["Justify"]))
    elems.append(Spacer(1, 20))

    pdf.build(elems)
    return complete_file_path,file_name




if __name__ == "__main__":
    create_report()