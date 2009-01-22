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
                        h1mozilla : { arguments : ['h4'], tags : ['h4'] },
                        h2mozilla : { arguments : ['h5'], tags : ['h5'] },
                        h3mozilla : { arguments : ['h6'], tags : ['h6'] },

                        h1 : { arguments : ['Heading 4'], tags : ['h4'] },
                        h2 : { arguments : ['Heading 5'], tags : ['h5'] },
                        h3 : { arguments : ['Heading 6'], tags : ['h6'] },

                        increaseFontSize : { visible : false },
                        decreaseFontSize : { visible : false },
                        separator09 : { visible : false }
                    }
                });
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
