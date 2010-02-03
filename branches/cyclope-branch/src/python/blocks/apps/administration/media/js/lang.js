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
		//console.debug("O: " + html);
		
		xp = get_xhtml_parser();
		html = xp.parse(html);
		
		html = html.replace("§BR§", "<br />");
		
		//console.debug("M: " + html);
	
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
				        // wymeditor_filebrowser(wym, wdw);
				        
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
