fetch("/config")
.then((result) => {  return result.json(); })
.then((data) => {
  const stripe = Stripe(data.publicKey);
  document.querySelector("#submitBtn").addEventListener("click", () => {
    fetch("/create_checkout_session")
    .then((result) => {return result.json(); })
    .then((data) => {
      return stripe.redirectToCheckout({ sessionId: data.sessionId })
    })
    .then((res) => {
       console.error(res);
    });
  });
});
