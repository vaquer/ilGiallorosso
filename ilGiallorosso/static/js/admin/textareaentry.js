$(document).ready(function(){
    if($("#id_text").length > 0){
        CKEDITOR.replace('id_text', {
            language: 'es',
            allowedContent: true,
            uiColor: '#9AB8F3'
        });
    }

    if($("#id_short_about").length > 0){
        CKEDITOR.replace('id_short_about', {
            language: 'es',
            allowedContent: true,
            uiColor: '#9AB8F3'
        });
    }
});
