$(document).ready(function(){
	$("#languages > ul").tabs();

    // this is a bit stupid but for now it works fine
    var __lang = $("#languages input.translations-language");
    $("#languages div.fld_language > select").each(function(index)
    {
        $(this).attr("value", __lang.get(index).value);
    });
});
