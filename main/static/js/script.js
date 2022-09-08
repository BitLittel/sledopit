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