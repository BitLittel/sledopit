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
    let loginPassword = document.getElementById('loginPassword').value,
        send_data = (loginPassword !== "") ? {phoneNumber: phoneNumber.value, loginPassword: loginPassword} : {phoneNumber: phoneNumber.value};
    console.log(phoneNumber, loginPassword, send_data)
    AJAX(
        {url: '/api/login', data: send_data},
        function (data) {
            if (loginPassword === "") {
                if (data.login == true) {document.getElementById('loginStep1').style.display = 'none';document.getElementById('loginStep2').style.display = 'block';}
                else if (data.login == false) {showErrorMessage(data.header, data.text);}
                else {document.getElementById('loginStep1').style.display = 'none';document.getElementById('loginStep3').style.display = 'block';}
            } else {
                if (data.login == true) {closeLoginPopUp();window.location.reload();}
                else {showErrorMessage(data.header, data.text);}
            }
        }
    );
}

function RegIn() {
    let name = document.getElementById('name'),
        signinPassword = document.getElementById('signinPassword'),
        personalDataAgreement = document.getElementById('personalDataAgreement');
    if (name.value == '') {showErrorMessage('Ошибка', 'Поле "Фамилия Имя" введено некорректно');}
    else {
        AJAX({url: '/api/reg', data: {phoneNumber: phoneNumber.value, name: name.value, signinPassword: signinPassword.value, personalDataAgreement: personalDataAgreement.checked}},
            function (data) {
                if (data.reg == false) {showErrorMessage(data.header, data.text);}
                else {closeLoginPopUp(); window.location.reload();}
            }
        );
    }
}

function addResearch(user_have_data, type_research, csrf_token) {
    let formData = new FormData(),
        text = document.getElementsByClassName('ck-editor__editable_inline')[0];
    if (text.innerText.length < 2000) {showErrorMessage('Ошибка', 'Дорогой друг, текст слишком короткий. Минимальная длина текста - 2000 символов.');return;}
    if (user_have_data == 'false') {
        let cityFrom = document.getElementById('cityFrom'),
            ageSelection = document.getElementById('ageSelection'),
            school = document.getElementById('school');
        if (cityFrom.value == null || cityFrom.value == '') {showErrorMessage('Ошибка', 'Поле "Откуда ты" не заполнено');return;}
        if (ageSelection.value == null || ageSelection.value == '') {showErrorMessage('Ошибка', 'Поле "Возраст" не заполнено');return;}
        if (school.value == null || school.value == '') {showErrorMessage('Ошибка', 'Поле "Учебное заведение" не заполнено');return;}
        formData.append('cityFrom', cityFrom.value);
        formData.append('ageSelection', ageSelection.value);
        formData.append('school', school.value);
    }
    let newResearchPhoto = document.getElementById('newResearchPhoto'),
        newResearchName = document.getElementById('newResearchName');
    if (newResearchName.value == null || newResearchName.value == '') {showErrorMessage('Ошибка', 'Поле "Название работы" не заполнено');return;}
    for (var i = 0, file; file = newResearchPhoto.files[i]; ++i) {formData.append('photo_and_video', file);}
    formData.append('newResearchText', text.innerHTML);
    formData.append('newResearchName', newResearchName.value);
    formData.append('have_data', user_have_data);
    formData.append('type_research', type_research);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/load_research', true);
    xhr.setRequestHeader("X-CSRFToken", csrf_token);

    xhr.onload = function(e) {
        showLoadMessage();
        if (xhr.status >= 200 && xhr.status < 400) {
            // выполнить при получении данных
            var result = JSON.parse(xhr.responseText);
            console.log(result);
            if (result.reseach == false) {showErrorMessage(result.header, result.text);}
            else {window.location.replace('/research/'+result.id_research)}
        } else {console.log(xhr.status);}
    }; xhr.send(formData);
}


function vote(id_research, is_authenticated, user_id) {
    let count_allow_votes = document.getElementById('count_allow_votes'),
        count_votes = document.getElementById('count_votes_'+id_research);
    if (is_authenticated == 'True') {
        AJAX({url: '/api/vote', data: {user_id: user_id, id_research: id_research}},
            function (data) {
                if (data.vote == true) {
                    count_allow_votes.innerText = Number(count_allow_votes.innerText) - 1;
                    count_votes.innerText = Number(count_votes.innerText) + 1;
                } else {showErrorMessage(data.header, data.text);}
            }
        )
    } else {showLoginPopUp(); showErrorMessage('Ошибка', 'Необходимо войти в аккаунт');}
}

function EditResearch(user_id, id_research) {
    let newResearchName = document.getElementById('newResearchName'),
        text = document.getElementsByClassName('ck-editor__editable_inline')[0];
    if (text.innerText.length < 2000) {showErrorMessage('Ошибка', 'Дорогой друг, текст слишком короткий. Минимальная длина текста - 2000 символов.');return;}
    if (newResearchName.value == null || newResearchName.value == '') {showErrorMessage('Ошибка', 'Поле "Название работы" не заполнено');return;}
    AJAX(
        {url: '/api/edit_research', data: {newResearchName: newResearchName.value, newResearchText: text.innerHTML, user_id: user_id, id_research: id_research}},
        function (data) {
            if (data.edit == true) window.location.replace('/research/'+id_research); else showErrorMessage(data.header, data.text);
        }
    );
}
