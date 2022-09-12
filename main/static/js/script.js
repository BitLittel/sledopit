function showHint() {
    document.getElementById("bgHeader").style.opacity = 0;
    document.getElementById("bgFooter").style.opacity = 0;
    document.getElementById("conBox").style.opacity = 0;
    document.getElementById("hintContainer").style.opacity = 1;
    document.getElementById("hintContainer").style.top = '0%';
    document.getElementById("hintContainer").style.transform = 'scale3d(1,1,1)';
    document.getElementById("fixed").style.opacity = 1;
    document.getElementById("fixed").style.bottom = '5%';
    document.getElementById("fixed").style.transform = 'scale3d(1,1,1)';
}

function closeHint() {
    document.getElementById("bgHeader").style.opacity = 1;
    document.getElementById("bgFooter").style.opacity = 1;
    document.getElementById("conBox").style.opacity = 1;
    document.getElementById("hintContainer").style.opacity = 0;
    document.getElementById("hintContainer").style.top = '100%';
    document.getElementById("hintContainer").style.transform = 'scale3d(2,0.5,3)';
    document.getElementById("fixed").style.opacity = 0;
    document.getElementById("fixed").style.bottom = '-5%';
    document.getElementById("fixed").style.transform = 'scale3d(2,0.5,3)';
}

window.addEventListener("DOMContentLoaded", function() {
    [].forEach.call( document.querySelectorAll('.tel'), function(input) {
        var keyCode;
        function mask(event) {
            event.keyCode && (keyCode = event.keyCode);
            var pos = this.selectionStart;
            if (pos < 3) event.preventDefault();
            var matrix = "+7 (___) ___ ____",
                i = 0,
                def = matrix.replace(/\D/g, ""),
                val = this.value.replace(/\D/g, ""),
                new_value = matrix.replace(/[_\d]/g, function(a) {
                    return i < val.length ? val.charAt(i++) || def.charAt(i) : a
                });
            i = new_value.indexOf("_");
            if (i != -1) {
                i < 5 && (i = 3);
                new_value = new_value.slice(0, i)
            }
            var reg = matrix.substr(0, this.value.length).replace(/_+/g,
                function(a) {
                    return "\\d{1," + a.length + "}"
                }).replace(/[+()]/g, "\\$&");
            reg = new RegExp("^" + reg + "$");
            if (!reg.test(this.value) || this.value.length < 5 || keyCode > 47 && keyCode < 58) this.value = new_value;
            if (event.type == "blur" && this.value.length < 5)  this.value = ""
        }

        input.addEventListener("input", mask, false);
        input.addEventListener("focus", mask, false);
        input.addEventListener("blur", mask, false);
        input.addEventListener("keydown", mask, false)

    });

});

function showLoginPopUp() {
    document.getElementById("bgHeader").style.opacity = 0;
    document.getElementById("bgFooter").style.opacity = 0;
    document.getElementById("conBox").style.opacity = 0;
    document.getElementById("loginPopUp").style.opacity = 1;
    document.getElementById("loginPopUp").style.marginTop = '0%';
    document.getElementById("loginPopUp").style.transform = 'scale(1)';
    document.getElementById("loginStep1").style.display = 'block';
    document.getElementById("loginStep2").style.display = 'none';
}

function closeLoginPopUp() {
    document.getElementById("bgHeader").style.opacity = 1;
    document.getElementById("bgFooter").style.opacity = 1;
    document.getElementById("conBox").style.opacity = 1;
    document.getElementById("loginPopUp").style.opacity = 0;
    document.getElementById("loginPopUp").style.marginTop = '-100%';
    document.getElementById("loginPopUp").style.transform = 'scale(4)';
}

function closeErrorMessage() {
    document.getElementById("errorBox").style.opacity = '0';
    document.getElementById("errorBox").style.top = '-100%';
}

function showErrorMessage(header, text) {
    document.getElementById("messageHeader").innerHTML = header;
    document.getElementById("messageText").innerHTML = text;
    document.getElementById("errorBox").style.opacity = '1';
    document.getElementById("errorBox").style.top = '50px';
    setTimeout(closeErrorMessage, 3000);
}

