window.jBus = window.jBus || {};
window.options = window.options || {};


(function ($, bus, opt) {

    bus.Place = function (options) {
        for (var opt in options) {
            this[opt] = options[opt];
        }

        this.initialize = function () {
            this.initMaps();
            this.initCoordAdd();
            this.initSubmit();
        };

        this.initialize_popup = function () {
            this.initMaps();
        };

        this.initSubmit = function () {
            this.bindMsg(this._submit_button, 'click', this.handlerSubmit, true);
        };

        this.initCoordAdd = function () {
            this.bindMsg(this._place_form, 'map_click', this.handlerCoordAdd, true);
        };

        this.handlerCoordAdd = function (event, target) {
            console.log(this.coords);
            $(this._place_latitude_field).val(this.coords[0]);
            $(this._place_longitude_field).val(this.coords[1]);
        };

        this.getFormData = function (target) {
            var form_data = $(target).serializeArray();
            console.log(form_data);
            var data = {};
            for (var i in form_data) {
                data[form_data[i].name] = form_data[i].value;
            }
            return data
        };

        this.handlerSubmit = function (event, target) {
            var place_form_data = this.getFormData(this._place_form);
            console.log(place_form_data);
            var action = this.get_action();
            var place_id = this.get_place_id();
            var url = this.get_url(action, place_id);
            $.ajax(
                {
                    context: this,
                    url: url,
                    method: 'POST',
                    async: true,
                    data: {
                        'place_data': JSON.stringify(place_form_data),
                        'csrfmiddlewaretoken': $(this._csrf_token).val()
                    },
                    success: function(res, textStatus) {
                        if (res['status'] === 302) {
                            window.location.href = res['redirect_uri'];
                        }
                        else {
                            $(this._form_tbody).html(res['tbody']);
                            this.initialize_popup();
                        }
                    },
                    complete: function (res) {

                    }
                }
            );
        };

        this.initMaps = function () {

            var obj = this;

            // Функция ymaps.ready() будет вызвана, когда
            // загрузятся все компоненты API, а также когда будет готово DOM-дерево.
            ymaps.ready(init);

            function init () {
                // Создание карты.
                var myMap = new ymaps.Map("map", {
                    // Координаты центра карты.
                    // Порядок по умолчанию: «широта, долгота».
                    // Чтобы не определять координаты центра карты вручную,
                    // воспользуйтесь инструментом Определение координат.
                    center: [55.76, 37.64],
                    // Уровень масштабирования. Допустимые значения:
                    // от 0 (весь мир) до 19.
                    zoom: 7
                });

                myMap.events.add('click', function (e) {
                    obj.coords = e.get('coords');
                    obj.publishMsg([obj._place_form], 'map_click');
                });
            }
        };

        this.setError = function (select, message) {
            $(select).html(message);
        };

        this.get_place_id = function () {
            return $(this._form).data('place_id');
        };

        this.get_action = function () {
            return $(this._form).data('action');
        };

        this.get_url = function (action, place_id) {
            var url =  this._url_base + action + '/popup/';
            if (place_id) {
                url = url + place_id + '/';
            }
            return url
        };

        this.delete = function () {

        };
    };

    (function (bus) {
        var channel_node = new bus.ChannelNode ();

        var place = new bus.Place({
            '_form': 'form',
            '_submit_button': 'button[type="submit"]',
            '_csrf_token': 'input[name=csrfmiddlewaretoken]',
            '_url_base': '/place/',
            '_form_tbody': '.tbody',

            '_place_form': '.place-form',
            '_place_latitude_field': 'input[name="latitude"]',
            '_place_longitude_field': 'input[name="longitude"]',

            '_errors_class': '.errors'
        });

        $.extend(true,
            place,
            channel_node);
        place.initialize();
    })(bus);

})(window.jQuery, window.jBus, options);