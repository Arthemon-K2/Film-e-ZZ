function isAlive(elem) {
    const h5 = elem.querySelector('.card-title')
    if (h5.getAttribute('data-alive') === 'yes') {
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

const rating = document.getElementById('show_rating').innerHTML
document.getElementById("stars").innerHTML = getStars(rating);

function getStars(rating) {

    // Round to nearest half
    rating = Math.round(rating) / 2;
    let output = [];

    // Append all the filled whole stars
    for (let i = rating; i >= 1; i--)
        output.push('<i class="fa fa-star" aria-hidden="true" style="color: gold;"></i>&nbsp;');

    // If there is a half a star, append it
    if (i == .5) output.push('<i class="fa fa-star-half-o" aria-hidden="true" style="color: gold;"></i>&nbsp;');

    // Fill the empty stars
    for (let i = (5 - rating); i >= 1; i--)
        output.push('<i class="fa fa-star-o" aria-hidden="true" style="color: gold;"></i>&nbsp;');

    return output.join('');

}