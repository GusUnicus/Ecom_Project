// function filterProducts(key) {
//     console.log(document.querySelectorAll('.dropdown-item'))
//     console.log(document.getElementById('product-list'))
//     var input, filter, ul, li, i, a, txtValue;
//     input = document.getElementById('search-input');
//     filter = input.value.toLowerCase();
//     ul = document.getElementById('product-list');
//     li = ul.getElementsByTagName('li');

//     for (i = 0; i < li.length; i++) {
//         a = li[i].getElementsByTagName('a')[0]; // Get the first <a> tag inside each <li>
//         txtValue = a.textContent || a.innerText;
//         if (txtValue.toLowerCase().indexOf(filter) > -1) {
//             li[i].style.display = '';
//         } else {
//             li[i].style.display = 'none';
//         }
//     }
// }

function filterProducts() {
    var input, filter, ul, li, a, i, txtValue;
    console.log(document.querySelectorAll('.dropdown-item'))
    input = document.getElementById("search-input");
    filter = input.value.toUpperCase();
    ul = document.getElementById("product-list");
    li = ul.getElementsByTagName("li");

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

// Event listener to show/hide the dropdown on input
document.getElementById("search-input").addEventListener("input", function () {
    var dropdownMenu = document.getElementById("dropdown-menu");
    dropdownMenu.classList.add("show");
});

// Event listener to hide the dropdown on clicking outside the input
document.addEventListener("click", function (event) {
    var dropdownMenu = document.getElementById("dropdown-menu");
    if (event.target !== document.getElementById("search-input")) {
        dropdownMenu.classList.remove("show");
    }
});