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

WYMeditor.XhtmlSaxListener.prototype.closeBlockTag = function(tag)
{
  this.output = this.output + this._getClosingTagContent('before', tag)+"</"+tag+">"+this._getClosingTagContent('after', tag);
};

function get_xhtml_parser()
{
	if (window.__XhtmlSaxListener__ == undefined)
	{
		var SaxListener_Ex = {
			remove_scripts: true,
			remove_embeded_styles: true,
			avoided_tags: ['div','span'],
			_avoiding_tags_implicitly: true,
			avoidStylingTagsAndAttributes: function() {},
			allowStylingTagsAndAttributes: function() {},
			openBlockTag: function(tag, attributes)
			{
				if (tag == "h1") tag = "h3";
				if (tag == "h2") tag = "h3";
				this.output += this.helper.tag(tag, this.validator.getValidTagAttributes(tag, attributes), true);
			},
			closeBlockTag: function(tag)
			{
				if (tag == "h1") tag = "h3";
				if (tag == "h2") tag = "h3";
				this.output = this.output + this._getClosingTagContent('before', tag)+"</"+tag+">"+this._getClosingTagContent('after', tag);
			}
		};
		var SL_validator = {
			skiped_attributes: ['style','class'],
			skiped_attribute_values: ['MsoNormal','main1']
		};
		
	    var sl = new WYMeditor.XhtmlSaxListener();
		$.extend(sl, SaxListener_Ex);
		$.extend(sl.validator, SL_validator);
		
		window.__XhtmlSaxListener__ = new WYMeditor.XhtmlParser(sl);
	}
	
	return window.__XhtmlSaxListener__;
}

function fixhtml(html, parser)
{
	if (html == "" || html == "<br />" ) return '';
	
	if (parser == undefined) parser = true;
	
	// check if content is formated
	if (html.substr(0, 1) != '<')
	{
		var pos = html.indexOf('<p>');
		if (pos == -1)
		{
			// no paragraphs assume it's text only
			
			var line = [];
			var sp = html.split("\n\n");	
			for(x = 0; x < sp.length; x++)
				if (sp[x] != "") line[x] = "<p>" + sp[x] + "</p>";
			html = line.join("");
			
			line = [];
			sp = html.split("<br /><br />");
			for(x = 0; x < sp.length; x++)
				if (sp[x] != "") line[x] = "<p>" + sp[x] + "</p>";
			html = line.join("");
		}
		
		// if has some paragraphs let's fix the start text
		else if (pos != -1 && pos + 1 != html.length)
		{
			var s1 = html.substring(0, pos);
			var s2 = html.substring(pos);
			html = '<p>' + s1 + '</p>' + s2;
		}
	}
	
	// check if last text is formatted
	if (html.substr(-4) != '</p>' && html.substr(html.length - 1) != '>')
	{
		var p1 = html.lastIndexOf('</');
		var p2 = html.lastIndexOf('>');
		if (p1 != -1 && p2 != -1 && p2 + 1 != html.length)
		{
			var s1 = html.substring(0, p2 + 1);
			var s2 = html.substring(p2 + 1);
			html = s1 + '<p>' + s2 + '</p>';
		}
	}
	
	// TODO: fix middle text formating (ex: </p>some text not wrapped<p>)
	
	// just in case of double formatting problems
	html = html.replace("<p><p>", "<p>");
	html = html.replace("</p></p>",  "</p>");

	if (parser)
	{
		html = html.replace("<br />", "§BR§");
		console.debug("O: " + html);
		
		xp = get_xhtml_parser();
		html = xp.parse(html);
		
		html = html.replace("§BR§", "<br />");
		
		console.debug("M: " + html);
	
		// if after the parser there's some problem with format then reformat
		if (html != "" && (html.substr(0, 1) != '<' || html.substr(html.length -1) != '>'))
			html = fixhtml(html, parser);
	}
	
	return html;
}

WYMeditor.editor.prototype.toggleHtml = function() {
	$(this._box).find(this._options.htmlSelector).toggle();
	$(this._box).find(this._options.toolSelector).each(function()
	{
		var tool = $(this);
		if (!tool.parent().hasClass("wym_tools_html"))
			tool.toggle();
	});
	var html = this.xhtml();
	this.html(fixhtml(html, false));
	this.update();
};

$(document).ready(
    function()
    {
        LOCALE_TABS = $("#languages > ul");

        LOCALE_TABS.initPanel__init = function(obj)
        {
        	if (obj[0]._WYM_ == undefined)
        	{
	        	obj.wymeditor({
	        		//lang: 'pt',
	        		logoHtml: '',
	        		
	        		toolsItems: [
			 			{'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'}, 
			 			{'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'},
			 			{'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'},
			 			{'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'},
			 			{'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'},
			 			{'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'},
			 			
			 			{'name': 'P',  'title': 'Paragraph', 'css': 'wym_tools_containerex para'},
			 			{'name': 'H3', 'title': 'Heading_3', 'css': 'wym_tools_containerex h3'},
			 			{'name': 'H4', 'title': 'Heading_4', 'css': 'wym_tools_containerex h4'},
			 			{'name': 'H5', 'title': 'Heading_5', 'css': 'wym_tools_containerex h5'},
			 			
			 			{'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'},
			 			{'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'},
			 			{'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'},
			 			{'name': 'Unlink', 'title': 'Unlink', 'css': 'wym_tools_unlink'},
			 			{'name': 'InsertImage', 'title': 'Image', 'css': 'wym_tools_image'},
			 			{'name': 'InsertTable', 'title': 'Table', 'css': 'wym_tools_table'},
			 			{'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'},
			 			{'name': 'ToggleHtml', 'title': 'HTML', 'css': 'wym_tools_html'}
	        		],
	
	        		classesItems: [],
	        		
	                updateSelector: "input:submit",
	                updateEvent:    "click",
	                
	                postInitDialog: function(wym, wdw)
	                {
						// the URL to the Django filebrowser, depends on your URLconf
						var fb_url = '/admin/filebrowser/';
						  
						var dlg = jQuery(wdw.document.body);
						if (dlg.hasClass('wym_dialog_image')) {
							// this is an image dialog
							var bt = dlg.find('.wym_src').css('width', '200px').attr('id', 'filebrowser');
							bt.after('<a id="fb_link" title="Filebrowser" href="#">Filebrowser</a>');
							
							var fs = dlg.find('fieldset');
							fs.append('<a id="link_filebrowser"><img id="image_filebrowser" /></a><br /><span id="help_filebrowser"></span>');
						
							dlg.find('#fb_link')
								.click(function() 
								{
									fb_window = wdw.open(fb_url + '?_popup=1&pop=1', 'filebrowser', 'height=600,width=840,resizable=yes,scrollbars=yes');
									fb_window.focus();
									return false;
								});
						}
	                },
	                
	                postInit: function(wym)
	                {
	                    // handle click event on containers buttons
						jQuery(wym._box).find('li.wym_tools_containerex a').unbind("click").click(function() {
							wym.container(jQuery(this).attr(WYMeditor.NAME));
							return(false);
						});
					
						// Filebrowser callback
				        wymeditor_filebrowser(wym, wdw);
				        
	                    //wym.hovertools();
	                    //wym.resizable();
	                    
	                    // fix content
	                    //console.debug(obj[0].id);
	                    //console.debug("XXX: " + wym.xhtml());
	                    
				 		wym.html(fixhtml(wym.xhtml(), false));
				 		wym.update();
	                    
	                    var editor = $(wym._doc.body);
	                    var element = $(wym._box).find(wym._options.htmlValSelector);
	                    
	                    editor.bind("paste", function()
	                    {
	                    	var last = wym.xhtml();
						 	setTimeout(function ()
						 	{
						 		var last = fixhtml(wym.xhtml());						 		
						 		wym.html(last);
						 		wym.update();
						 	}, 10);
	                    });
	                    /*
	                    element.bind("paste", function()
	                    {
	                    	var el = $(this);
	                    	var last = el.val();
						 	setTimeout(function ()
						 	{
						 		el.val(last);
						 	}, 10);
	                    });
	                    */
	                    
	                }
	            });
	        	
	        	obj[0]._WYM_ = true;
        	}
        };

        LOCALE_TABS.initPanel = function()
        {
            LOCALE_TABS.initPanel__init($(this));
        };

        LOCALE_TABS.tabs();

        var panel = $("#languages div.ui-tabs-panel")[LOCALE_TABS.data('selected.tabs')];
        $(panel).find("textarea.vLargeTextField").each(LOCALE_TABS.initPanel);

        LOCALE_TABS.bind('tabsshow',
            function(event, ui)
            {
                var panel = $("#languages div.ui-tabs-panel")[ui.index];
                $(panel).find("textarea.vLargeTextField").each(LOCALE_TABS.initPanel);
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
