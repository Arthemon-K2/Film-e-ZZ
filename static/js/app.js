function isAlive(elem) {
    const p = elem.querySelector('.age')
    if (p.getAttribute('data-alive') === 'yes') {
       elem.style.background = 'lightgreen';
    } else {
       elem.style.background = 'black';
       elem.style.color = 'white'
    }
}


function reset(elem) {
    elem.style.background = '#efefef'
    elem.style.color = 'black'

}

const modal = document.getElementById('modal_YT_trailer');
const button_to_modal = document.getElementById('watch-trailer');
const span = document.getElementsByClassName("close")[0];

button_to_modal.onclick = function () {
    modal.style.display = 'block';
}

span.onclick = function () {
    modal.style.display = 'none';
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

