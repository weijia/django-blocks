$(document).ready(
    function()
    {
        var __maps = $("form div.form-row div.gmap");
        __maps.each
        (function(index)
        {
            var name = $(this).attr("id").substring(4);
            var fnc = window["load_" + name];
            if (typeof fnc == "function") fnc();
        });
    }
);
