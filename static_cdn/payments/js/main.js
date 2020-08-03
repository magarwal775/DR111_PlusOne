let stripe = null;

fetch("/config/").then((res) => { return res.json(); })
    .then((data) => {
        stripe = Stripe(data.public_key);
    });

$(document).ready(function () {
    $('#dono_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: 'post',
            url: '/create-checkout-session/',
            contentType: "application/x-www-form-urlencoded",
            success: function (res) {
                console.log(res);
                return stripe.redirectToCheckout({ sessionId: res.sessionId });
            },
            error: function (err) {
                console.log(err);
            }
        });
    });
});