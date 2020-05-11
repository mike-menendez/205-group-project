// mapping of country to country code
var countries = null

$(document).ready(() => {
    $(".search").on("click", () => {
        if (countries == null) { $.ajax({ url: window.location.href + "preload", async: false, success: (res) => { countries = res } }) }
        country = $("input").val();
        country.trim().toLowerCase().replace(/ /g, "-") in countries ?
            window.location.href = "/country/" + countries[country.trim().toLowerCase().replace(/ /g, "-")].toLowerCase() :
            Swal.fire({ title: 'Invalid Country Requested', icon: 'error', text: 'Please Try Again' });
    });

    $(".dcard").on("click", () => {
        window.location.href = "/all/deaths";
    });
    $(".ccard").on("click", () => {
        window.location.href = "/all/confirmed";
    });
    $(".rcard").on("click", () => {
        window.location.href = "/all/recovered";
    });
});