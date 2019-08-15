window.jBus = window.jBus || {};
window.options = window.options || {};


(function ($, bus, opt) {

    bus.PlacesList = function (options) {
        for (var opt in options) {
            this[opt] = options[opt];
        }

        this.initialize = function () {
            this.initUpdateLinks();
            this.initDeleteLinks();
        };

        this.initialize_popup = function () {

        };

        this.get_url = function (action, place_id, popup) {
            var url =  this._url_base + action + '/';
            if (popup) {
                url = url + 'popup/';
            }
            if (place_id) {
                url = url + place_id + '/';
            }
            return url
        };

        this.initUpdateLinks = function () {
            this.bindMsg(this._place_update_link, 'click', this.handlerPlaceUpdateLink, true);
        };

        this.initDeleteLinks = function () {
            this.bindMsg(this._place_delete_link, 'click', this.handlerPlaceDeleteLink, true);
            this.bindMsg(this._place_delete_modal_button, 'click', this.handlerPlaceDeleteSubmit, true);
        };

        this.handlerPlaceUpdateLink = function (event, target) {
            var place_id = $(target).data('place_id');
            var action = 'update';
            window.location.href = this.get_url(action, place_id);
        };

        this.handlerPlaceDeleteSubmit = function () {
            var place_id = this.place_index_temp;
            var action = 'delete';
            this.ajaxPlaceRequest(action, place_id);
            $(this._place_delete_modal).modal('hide');
        };

        this.handlerPlaceDeleteLink = function (event, target) {
            $(this._place_delete_modal).modal('show');
            this.place_index_temp = $(target).data('place_id');
        };

        this.ajaxPlaceRequest = function (url_action, place_id) {
            var url = this.get_url(url_action, place_id, true);
            $.ajax(
                {
                    context: this,
                    url: url,
                    method: 'POST',
                    async: true,
                    data: {
                        'csrfmiddlewaretoken': $(this._csrf_token).val()
                    },
                    success: function(res, textStatus) {
                        if (res['status'] === 302) {
                            window.location.href = res['redirect_uri'];
                        }
                    },
                    complete: function (res) {

                    }
                }
            );
        };
    };

    (function (bus) {
        var channel_node = new bus.ChannelNode ();
        var data_storage = new bus.DataHtmlStorage();

        var place_list = new bus.PlacesList({
            '_place_update_link': '.place-update-link',
            '_place_delete_link': '.place-delete-link',
            '_url_base': '',
            '_place_delete_modal': '#place-delete-modal',
            '_place_delete_modal_button': '.modal-button-submit',
            '_csrf_token': 'input[name=csrfmiddlewaretoken]'
        });

        $.extend(true,
            place_list,
            channel_node,
            data_storage);
        place_list.initialize();
    })(bus);

})(window.jQuery, window.jBus, options);
