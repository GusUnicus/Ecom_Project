var shoppingCart = (function() {

  cart = [];
  
  function Item(name, price, count) {
    this.name = name;
    this.price = price;
    this.count = count;
  }
  
  function saveCart() {
    sessionStorage.setItem('shoppingCart', JSON.stringify(cart));
  }
  
  function loadCart() {
    cart = JSON.parse(sessionStorage.getItem('shoppingCart'));
  }
  if (sessionStorage.getItem("shoppingCart") != null) {
    loadCart();
  }
  

  var obj = {};
  
  obj.addItemToCart = function(name, price, count) {
    for(var item in cart) {
      if(cart[item].name === name) {
        cart[item].count ++;
        saveCart();
        return;
      }
    }
    var item = new Item(name, price, count);
    cart.push(item);
    saveCart();
  }

  obj.setCountForItem = function(name, count) {
    for(var i = 0; i < cart.length; i++) {
      if (Object.prototype.hasOwnProperty.call(cart[i], 'name') && cart[i].name === name) {
        cart[i].count = count;
        break;
      }
    }
  };

  obj.removeItemFromCart = function(name) {
      for(var item in cart) {
        if(cart[item].name === name) {
          cart[item].count --;
          if(cart[item].count === 0) {
            cart.splice(item, 1);
          }
          break;
        }
    }
    saveCart();
  }

  obj.removeItemFromCartAll = function(name) {
    for(var item in cart) {
      if(cart[item].name === name) {
        cart.splice(item, 1);
        break;
      }
    }
    saveCart();
  }

  obj.clearCart = function() {
    cart = [];
    saveCart();
  }

  obj.totalCount = function() {
    var totalCount = 0;
    for(var item in cart) {
      totalCount += cart[item].count;
    }
    return totalCount;
  }

  obj.totalCart = function() {
    var totalCart = 0;
    for(var item in cart) {
      totalCart += cart[item].price * cart[item].count;
    }
    return Number(totalCart.toFixed(2));
  }

  obj.listCart = function() {
    var cartCopy = [];
    for(i in cart) {
      item = cart[i];
      itemCopy = {};
      for(p in item) {
        itemCopy[p] = item[p];

      }
      itemCopy.total = Number(item.price * item.count).toFixed(2);
      cartCopy.push(itemCopy)
    }
    return cartCopy;
  }

// JS for modal pop to show item has been added to the cart.
document.querySelector('.add-to-cart').addEventListener('click', function() {
  var myModal = new bootstrap.Modal(document.getElementById('cartModal'), {});
  myModal.show();
});

// JS for modal pop to show item has been added to the cart.
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.add-to-cart').forEach(function(button) {
      button.addEventListener('click', function(event) {
          event.preventDefault();
          var myModal = new bootstrap.Modal(document.getElementById('cartModal2'));
          myModal.show();
      });
  });
});

// JS for sorting products in shop.html
const productList = document.getElementById("product-list");
const originalProducts = Array.from(productList.children);
document.getElementById("sort-select").addEventListener("change", function() {

  let products = Array.from(originalProducts);

  if (this.value === "a_to_z") {
    products.sort((a, b) => {
        const titleA = a.querySelector(".h3").textContent.toLowerCase();
        const titleB = b.querySelector(".h3").textContent.toLowerCase();
        return titleA.localeCompare(titleB);
    });
  } else if (this.value === "featured") {
    products = products.filter(product => {
        const title = product.querySelector(".add-to-cart").getAttribute("data-name").toLowerCase();
        return title.includes("gucci") || title.includes("lv") || title.includes("chanel");
    });
  }

  // Clear the product list and append filtered/sorted elements back to the DOM
  while (productList.firstChild) {
      productList.removeChild(productList.firstChild);
  }
  
  products.forEach(product => productList.appendChild(product));
});



  return obj;
})();


$('.add-to-cart').click(function(event) {
  event.preventDefault();
  var name = $(this).data('name');
  var price = Number($(this).data('price'));
  shoppingCart.addItemToCart(name, price, 1);
  displayCart();
});

$('.clear-cart').click(function() {
  shoppingCart.clearCart();
  displayCart();
});


function displayCart() {
  var cartArray = shoppingCart.listCart();
  var output = "";
  for(var i in cartArray) {
    output += "<tr>"
      + "<td>" + cartArray[i].name + "</td>" 
      + "<td>(" + cartArray[i].price + ")</td>"
      + "<td><div class='input-group'><button class='minus-item input-group-addon btn btn-primary' data-name='" + cartArray[i].name + "'><i class='fas fa-minus'></i></button>"
      + "<input type='text' class='item-count form-control text-center' data-name='" + cartArray[i].name + "' value='" + cartArray[i].count + "'>"
      + "<button class='plus-item btn btn-primary input-group-addon' data-name='" + cartArray[i].name + "'><i class='fas fa-plus'></i></button></div></td>"
      + "<td><button class='delete-item btn btn-danger' data-name='" + cartArray[i].name + "'><i class='fas fa-times'></i></button></td>"
      + " =  " 
      + "<td>" + cartArray[i].total + "</td>" 
      +  "</tr>";
  }
  $('.show-cart').html(output);
  $('.total-cart').html(shoppingCart.totalCart());
  $('.total-count').html(shoppingCart.totalCount());
}


$('.show-cart').on("click", ".delete-item", function(event) {
  var name = $(this).data('name')
  shoppingCart.removeItemFromCartAll(name);
  displayCart();
})


$('.show-cart').on("click", ".minus-item", function(event) {
  var name = $(this).data('name')
  shoppingCart.removeItemFromCart(name);
  displayCart();
})

$('.show-cart').on("click", ".plus-item", function(event) {
  var name = $(this).data('name')
  shoppingCart.addItemToCart(name);
  displayCart();
})



$('.show-cart').on("change", ".item-count", function(event) {
   var name = $(this).data('name');
   var count = Number($(this).val());
  shoppingCart.setCountForItem(name, count);
  displayCart();
});

displayCart();

function sendCartToBackend(cartData) {
  fetch('/cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(cartData)
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
}

document.querySelector('.checkout-btn').addEventListener('click', function(event) {
  event.preventDefault();
  var cartData = shoppingCart.listCart();
  sendCartToBackend(cartData);
});

