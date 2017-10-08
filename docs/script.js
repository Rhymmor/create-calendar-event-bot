window.onload = init;

function getQueryVariable(variable) {
    const query = window.location.search.substring(1);
    const vars = query.split('&');
    for (const x of vars) {
        const pair = x.split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.error(`Query variable ${variable} not found`);
}

function init() {
    const code = getQueryVariable('code');
    const elem = document.getElementById('code');
    if (code) {
        elem.textContent = code;
        copyByClick(elem);
    } else {
        elem.textContent = 'There is no code for you';
    }
}

function copyByClick(elem) {
    elem.onclick = () => document.execCommand('copy');
    elem.addEventListener("copy", (event) => {
        event.preventDefault();
        if (event.clipboardData) {
            event.clipboardData.setData("text/plain", elem.textContent);
        }
    });
}