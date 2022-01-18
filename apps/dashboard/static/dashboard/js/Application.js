$( document ).ready(function() {
//setting event with input field for detecting number of application fields
$("#number_videos").on("change",function(){
parent_div = $('#space')
number_videos = $(this).val()
$(".video-js").each(function(){
$(this).remove();
})
for(i=0;i<number_videos;i++){
let field_parent = $('<div class="mt-2 video-js"></div>')
let new_field_label = $('<label for="number_'+i+'" class="requiredField"></label>')
new_field_label.html('Application Video ['+(i+1)+']<span class="asteriskField">*</span>')
let new_input_field = $('<input type="url" name="video" autofocus  class="form-control" required id="number_'+i+'">')
$(field_parent).append(new_field_label)
$(field_parent).append(new_input_field)
$(parent_div).append(field_parent)

}
});
});