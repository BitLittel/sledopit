/**
 * Created by linea on 12.06.2017.
 * by Vladislav
 */


/**
 * Получение и отправка данных AJAX
 * @param {Object} data Параметры запроса
 *   @param {String} [data.url=document.location] URL запроса
 *   @param {String} [data.method="GET"] Метод запроса (GET или POST]
 *   @param {String} [data.dataType="json"] Формат получаемых данных
 *   @param {(Object|String)} data.data Данные запроса в виде объекта или сериализованной строки
 *   @param {Boolean} [data.async=true] Выполнить запрос асинхронно
 * @param {Function} [onsuccess] Функция, вызываемая в случае успешного запроса
 * @param {Function} [onerror] Функция, вызываемая при ошибке
 *
 * @author Vladislav
 * @version 0.1
 */
var AJAX = function(data, onsuccess, onerror){
    if (!data) {
        data = {};
    }
    data.url = data.url || document.location;
    data.method = data.method || 'GET';
    data.dataType = data.dataType || 'json';
    data.data = data.data || false;
    data.async = typeof data.async == 'boolean' ? data.async : true;

    data.method = data.method.toUpperCase();

    function sender() {
        var request = new XMLHttpRequest();
        // обработка ответа
        request.onload = function() {
            if (request.status >= 200 && request.status < 400) {
                // выполнить при получении данных
                if (onsuccess) {
                    var result;
                    if (data.dataType.toLowerCase() == 'json') {
                        // парсинг JSON в объект
                        result = JSON.parse(request.responseText);
                    } else {
                        // удаление комментариев из html
                        var re = /<!--.*?-->/g;
                        result = request.responseText;
                        result = result.replace(re, '');
                    }
                    // пользовательская функция обработки данных
                    onsuccess(result);
                }
            } else {
                // выполнить при ошибке получения данных
                if (onerror) {
                    onerror(request.status);
                }
            }
        };
        var num = 0;
        request.onerror = function() {
            // выполнить при ошибке запроса
            if (onerror) {
                onerror(request.status);
            } else {
                if (num < 10) {
                    sender();
                }
            }
        };
        if (data.data) {
            // если есть данные для отправки
            var body = '';
            if (typeof(data.data) == "object") {
                // сериализация данных
                body = Object.keys(data.data).map(function(key) {
                    return key + '=' + encodeURIComponent(data.data[key]);
                }).join('&');
            } else {
                body = data.data;
            }
            if (data.method == 'POST') {
                // отправка методом POST
                request.open('POST', data.url, true);
                request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                request.send(body);
            } else {
                // отправка методом GET
                request.open('GET', data.url + '?' + body, true);
                request.send();
            }
        } else {
            // отправка пустого запроса
            request.open(data.method, data.url, data.async);
            request.send();
        }
    }
    sender();
};


/**
 * Сериализация данных формы
 * @param {object} form Объект DOM
 * @returns {string} Сериализованная строка данных
 *
 * @author Vladislav
 * @version 0.1
 */
var Serialize = function(form) {
    function text(e){
        if ( e.value !== '' ) {
            return [e.name + '=' + encodeURIComponent(e.value)];
        } else {
            return [];
        }
    }
    function select(e){
        var array = [],
            options = e.selectedOptions;
        if ( options.length ) {
            for (var i=0; i<options.length; i++) {
                array[array.length] = e.name + '=' + encodeURIComponent(options[i].value);
                if ( i+1 == options.length ) {
                    return array;
                }
            }
        } else {
            return array;
        }
    }
    function checkbox(e){
        if ( e.checked ) {
            return [e.name + '=' + encodeURIComponent(e.value)];
        } else {
            return [];
        }
    }
    var array = [],
        elements = form.querySelectorAll('input,textarea,select');
        for (var i=0; i<elements.length; i++) {
            var newVal;
            switch ( elements[i].tagName.toLowerCase()  ) {
                case 'select':
                    newVal = select(elements[i]);
                    break;
                case 'textarea':
                    newVal = text(elements[i]);
                    break;
                default:
                    switch ( elements[i].type.toLowerCase()  ) {
                        case 'checkbox':
                        case 'radio':
                            newVal = checkbox(elements[i]);
                            break;
                        default:
                            newVal = text(elements[i]);
                    }
            }
            if ( newVal && newVal.length > 0 ) {
                array = array.concat(newVal);
            }
            if ( i+1 == elements.length ) {
                return array.join('&');
            }
        }
};


let phoneNumber;

function logIn() {
    phoneNumber = document.getElementById('phoneNumber');
    AJAX(
        {
            url: '/api/login',
            data: {
                phoneNumber: phoneNumber.value
            }
        },
        function (data) {
            if (data.login == true) {
                closeLoginPopUp();
                window.location.reload();
            } else if (data.login == false) {
                showErrorMessage(data.header, data.text);
            } else {
                document.getElementById('loginStep1').style.display = 'none';
                document.getElementById('loginStep2').style.display = 'block';
            }
        }
    );
}

function RegIn() {
    let name = document.getElementById('name'),
        school = document.getElementById('school'),
        ageSelection = document.getElementById('ageSelection'),
        cityFrom = document.getElementById('cityFrom'),
        personalDataAgreement = document.getElementById('personalDataAgreement');
    if (name.value == '') {
        showErrorMessage('Ошибка', 'Поле "Фамилия Имя" введено некорректно');
    } else if (school.value == '') {
        showErrorMessage('Ошибка', 'Поле "Школа" введено некорректно');
    } else if (ageSelection.value == '') {
        showErrorMessage('Ошибка', 'Поле "Возраст" введено некорректно');
    } else if (cityFrom.value == '') {
        showErrorMessage('Ошибка', 'Поле "Откуда ты" введено некорректно');
    } else if (!personalDataAgreement.checked) {
        showErrorMessage('Ошибка', 'Извините, без вашего согласия на обработку, мы не можем вас зарегистрировать');
    } else {
        AJAX(
            {
                url: '/api/reg',
                data: {
                    phoneNumber: phoneNumber.value,
                    name: name.value,
                    school: school.value,
                    ageSelection: ageSelection.value,
                    cityFrom: cityFrom.value,
                    personalDataAgreement: personalDataAgreement.checked
                }
            },
            function (data) {
                if (data.reg == false) {
                    showErrorMessage(data.header, data.text);
                } else {
                    closeLoginPopUp();
                    window.location.reload();
                }
            }
        );
    }
}
