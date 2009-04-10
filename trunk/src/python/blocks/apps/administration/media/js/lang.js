function showPopupImage(url)
{
    var el = $('#show_image_popup');
    if (el.length == 0)
    {
        var popup = '<div id="show_image_popup" class="popup">';
        popup += '   <img src="' + url + '"/>';
        popup += '</div>';

        $(popup).appendTo("body");

        el = $('#show_image_popup');
   }

    if (el.length > 0)
    {
        $.blockUI({
            message: el,
            applyPlatformOpacityRules: false,
            css: { width: 'auto', backgroundColor: 'black', borderColor: 'black' },
            overlayCSS: { opacity: 0.4 }
        });
        //make the cursor be a hand when hovering over it
        el.css("cursor","pointer").css("cursor","hand");
        el.click($.unblockUI);
    }
}

$.popup = function()
{
    var SELF = $(this)[0];
    var selection = SELF.editor.documentSelection();

    var elm = $.data(SELF.editor, 'element.createLink');
    elm = elm != null && elm.tagName != null && elm.tagName.toUpperCase() == "A" ? elm : null;
    if (elm == null && selection.length <= 0)
    {
        if (SELF.options.messages.nonSelection)
            alert(SELF.options.messages.nonSelection);
        return;
    }

    var el = $('#json_image_popup');
    var opt_inp = null;
    var url_inp = null;
    if (el.length == 0)
    {
        var popup = '<div id="json_image_popup" class="popup">';
        popup += '   <fieldset class="aligned">';
        popup += '      <h2>Link Properties</h2>';
        popup += '      <div class="form-row">';
        popup += '         <label class="required" for="json_image_popup_type">Type:</label>';
        popup += '         <select id="json_image_popup_type"></select>';
        popup += '      </div>';
        popup += '      <div class="form-row template">';
        popup += '         <label class="required" for="json_image_popup_url">Url:</label>';
        popup += '         <input id="json_image_popup_url" class="vTextField" />';
        popup += '         <p class="help">Internal: some/page, External: www.example.com, E-Mail: user@example.com</p>';
        popup += '      </div>';
        popup += '   </fieldset>';
        popup += '   <div class="submit-row">';
        popup += '      <input id="json_image_popup_ok" type="button" value="OK" />';
        popup += '      <input id="json_image_popup_cancel" type="button" value="Cancel" />';
        popup += '   </div>';
        popup += '</div>';

        $(popup).appendTo("body");

        el = $('#json_image_popup');

        opt_inp = $(el).find("#json_image_popup_type");
        url_inp = $('#json_image_popup');
        opt_inp.addOption({
            "/"        : "Internal (Relative)",
            "http://"  : "External (HTTP)",
            "https://" : "External (HTTPS/SSL)",
            "mailto:"  : "E-Mail",
            ""         : "Custom"
        }, false);

        el[0]._ctr = SELF;
        if ( $.browser.msie && SELF.editor[0].contentWindow.document.selection)
            el[0]._sel =  SELF.editor[0].contentWindow.document.selection.createRange();

        el.unblock_json = function()
        {
            $.unblockUI({
                onUnblock: function()
                {
                    var o = $('#json_image_popup')[0];
                    var t = $(o).find("#json_image_popup_type").val();
                    var u = $(o).find("#json_image_popup_url").val();

                    if (u != "" && u.length > 0)
                    {
                        $.url.setUrl(u);
                        var proto = $.url.attr("protocol");
                        if (proto == "http" || proto == "https")
                        {
                            u = u.substr(proto.length + 2);
                            if (u.substr(0,1) == '/') u = u.substr(1);
                        }
                        if (t == "/" && u.substr(-1) != '/') u += '/';
                        if (t != "" && u.substr(0,1) == '/') u = u.substr(1);

                        var url = t  + u;
                        
                        var elm = $.data(o._ctr.editor, 'element.createLink');
                        elm = elm != null && elm.tagName != null && elm.tagName.toUpperCase() == "A" ? elm : null;
                        if (elm != null)
                            $(elm).attr("href", url);
                        else
                        {
                            if ( $.browser.msie )
                            {
                                var sel = o._sel;
                                sel.pasteHTML('<a href="' + url + '">' + sel.text + '</a>');
                                sel.select();
                                //o._ctr.editorDoc.execCommand('createLink', true, null);
                            }
                            else
                            {
                                o._ctr.editorDoc.execCommand('unlink', false, []);
                                o._ctr.editorDoc.execCommand('createLink', false, url);
                            }
                        }
                    }
                }
            });
        };

        $("#json_image_popup_ok").click(el.unblock_json);
        $("#json_image_popup_cancel").click($.unblockUI);
    }
    else
        opt_inp = $(el).find("#json_image_popup_type");
        url_inp = $("#json_image_popup_url");

    opt_inp.selectOptions("/");
    url_inp.val("");

    if (el.length > 0)
    {
        if (elm)
        {
            var ret = $(elm).attr("href");
            if (ret !== null)
            {
                var url = ret;
                $.url.setUrl(url);
                var proto = $.url.attr("protocol");
                var type = "";
                if (proto == null && $.url.attr("user") == "mailto")
                {
                    type = "mailto:";
                    url = url.substr(7);
                }
                else if (proto == "http" || proto == "https")
                {
                    type = proto + "://";
                    url = url.substr(proto.length + 2);
                    if (url.substr(0,1) == '/') url = url.substr(1);
                }
                else if (proto == null && $.url.attr("path") != null)
                    type = "/";

                opt_inp.selectOptions(type);
                url_inp.val(url);
            }
        }
        $.blockUI({
            message: el,
            applyPlatformOpacityRules: false,
            css: { borderColor: 'black' },
            overlayCSS: { opacity: 0.4 }
        });
    }
};

$(document).ready(
    function()
    {
        LOCALE_TABS = $("#languages > ul")

        LOCALE_TABS.initPanel__init = function(obj)
        {
            if (obj.attr("wysiwyg") == null)
            {
                obj.attr("wysiwyg", true);
                $(obj).wysiwyg(
                {
                    css: MEDIA_URL + 'css/typography.css',
                    
                    controls:
                    {
                        createLink : { exec : $.popup },
                        insertImage: { visible: false },

                        h1mozilla : { arguments : ['h4'], tags : ['h4'] },
                        h2mozilla : { arguments : ['h5'], tags : ['h5'] },
                        h3mozilla : { arguments : ['h6'], tags : ['h6'] },

                        h1 : { arguments : ['Heading 4'], tags : ['h4'] },
                        h2 : { arguments : ['Heading 5'], tags : ['h5'] },
                        h3 : { arguments : ['Heading 6'], tags : ['h6'] },

                        increaseFontSize : { visible : false },
                        decreaseFontSize : { visible : false },
                        separator09 : { visible : false },

                        html : {
                        	visible : true,
                            exec    : function()
                            {
                                if ( this.viewHTML )
                                {
                                    this.setContent( $(this.original).val() );
                                    $(this.original).hide();
                                    $(this.editor).show();
                                }
                                else
                                {
                                    this.saveContent();
                                    $(this.original).show();
                                    $(this.editor).hide();
                                }

                                this.viewHTML = !( this.viewHTML );
                            }
                        }
                    }
                });
                
                try
                {
                	var ed = $.data(obj[0], 'wysiwyg');				
					$(ed.editorDoc).bind('paste', function(ev)
					{
					 	var me = $(this).find('body');
					 	setTimeout(function ()
					 	{
					 		var html = me.html();
					 		me.html($.htmlClean(html))
					 	}, 100);
					});
					$(ed.original).bind('paste', function(ev)
					{
					 	var me = $(this);
					 	setTimeout(function ()
					 	{
					 		var html = me.val();
					 		me.val($.htmlClean(html))
					 	}, 100);
					});
					ed.editorDoc.execCommand('styleWithCSS', false, false);
					
                } catch(ex){}
            }
        };

        LOCALE_TABS.initPanel = function()
        {
            LOCALE_TABS.initPanel__init($(this));
        };

        LOCALE_TABS.tabs();

        var panel = $("#languages div.ui-tabs-panel")[LOCALE_TABS.data('selected.tabs')];
        $(panel).find("textarea").each(LOCALE_TABS.initPanel);

        LOCALE_TABS.bind('tabsshow',
            function(event, ui)
            {
                var panel = $("#languages div.ui-tabs-panel")[ui.index];
                $(panel).find("textarea").each(LOCALE_TABS.initPanel);
            }
        );

        // this is a bit stupid but for now it works fine
        var __lang = $("#languages input.translations-language");
        $("#languages div.fld_language > select").each(function(index)
        {
            $(this).attr("value", __lang.get(index).value);
        });
    }
);
