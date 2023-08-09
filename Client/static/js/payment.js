fetch("/config")
.then((result) => { return result.json(); })
.then((data) => {
  const stripe = Stripe(data.publicKey);
  document.querySelector("#submitBtn").addEventListener("click", () => {
    console.log('Test 3, button pressed')
    // Get Checkout Session ID
    fetch("/create_checkout_session")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});