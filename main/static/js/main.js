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

let registred = false,
    first_quastion = false;

// funButton flatButton funButtonSmall
window.addEventListener("load", function(event) {
    // на все кнопки вешаем функцию входа/регистрации если пользователь не зареган
    if (registred === false) {
        let funButton = document.getElementsByClassName('funButton'),
            flatButton = document.getElementsByClassName('flatButton'),
            funButtonSmall = document.getElementsByClassName('funButtonSmall'),
            func = function(){document.getElementById('login_popup').style.display = 'block';};

        for (var i = 0; i < funButton.length; i++) {
            funButton[i].addEventListener('click', func);
        }
        for (var j = 0; j < flatButton.length; j++) {
            flatButton[j].addEventListener('click', func);
        }
        for (var k = 0; k < funButtonSmall.length; k++) {
            funButtonSmall[k].addEventListener('click', func);
        }
    } else {
        console.log('Тут начинаем голосование')
    }

    // вешаем обработку на окно входа, что если нажимаем вне окна, оно скрываеться(да нужно вылавливать через evenTarget)
    document.getElementById('login_popup').addEventListener('click', function(event) {
        event = event || window.event;
        let target = event.target || event.srcElement;
        if (target == this) {
            this.style.display = 'none';
        }
    });


});




function quastion(answer) {
    document.getElementById('first_quastion').style.display = 'none';
    if (answer == true) {
        document.getElementById('send_button').innerText = 'Зарегестрироваться';
        first_quastion = true;
    } else {
        first_quastion = false;
        document.getElementById('city_input').style.display = 'none';
        document.getElementById('age_input').style.display = 'none';
        document.getElementById('personal_input').style.display = 'none';
        document.getElementById('send_button').innerText = 'Войти';
    }
}


function logIn() {
    let form_reg_log = document.getElementById('form_reg_log');
    AJAX({url: '/main', data: Serialize(form_reg_log)});
    console.log(Serialize(form_reg_log));
}


// function login() {
//     let FIO = document.getElementById('FIO'),
//         tel = document.getElementById('tel'),
//         form = document.getElementById('form_reg');
//     AJAX({url: "/login", data: {FIO: FIO.value, tel: tel.value}},
//         function (data) {
//             if (data) {
//                 if (data.reg_ok == false) {
//                     if (data.input == 'fio') {
//                         FIO.style.border = '2px solid #FF3838';
//                         document.getElementById('input_login').style.display = 'block';
//                     }
//                     if (data.input == 'tel') {
//                         tel.style.border = '2px solid #FF3838';
//                         document.getElementById('input_password').style.display = 'block';
//                     }
//                 } else {
//                     form.submit();
//                 }
//             } else {
//                 console.log('Ошибка соеденения')
//             }
//         }
//     );
// }