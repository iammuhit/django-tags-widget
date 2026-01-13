(function($) {
    'use strict';

    $(document).ready(function() {
        const $fields = $('input[data-provides="mayacms.forms.widgets.tags"]');

        $fields.each(function (idx, elem) {
            const $field = $(elem);

            const readonly = $field.attr('readonly') ?? undefined;
            const disabled = $field.attr('disabled') ?? undefined;

            if (readonly === undefined && disabled === undefined) {
                const config = {
                    enforceWhitelist: ($field.data('enforce') == 'true'),
                    dropdown: {
                        enabled: 0,
                    },
                };

                if ($field.data('options') != '[]') {
                    config.whitelist = JSON.parse(JSON.stringify($field.data('options')));
                }
                
                if ($field.data('max') != 'false') {
                    config.maxTags = $field.data('max');
                }

                const tags = new Tagify(elem, config);
            }
        });
    });

})(django.jQuery);
