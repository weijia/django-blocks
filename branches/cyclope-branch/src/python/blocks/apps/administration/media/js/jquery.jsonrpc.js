(function($)
{
    $.json = function(url, methodname, parameters, callback)
    {
        var request = {method: methodname, params: parameters, id: (new Date).getTime()};
        return $.post(url, $.toJSON(request), callback, 'json');
    }
})(jQuery);