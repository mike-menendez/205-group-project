// Authors: Mike Menendez, Frank Piva, Felix Romero-Flores, Edgaras Slezas
// Date: May 11, 2020
// Course: CST 205
// Description: Jquery and Ajax to support the site with on click listeners and fetching the data for the search bar
var countries = null
$(document).ready(() => {
    $(".search").on("click", () => {
        if (countries == null) { $.ajax({ url: window.location.href + "preload", async: false, success: (res) => { countries = res } }) }
        country = $("input").val();
        country.trim().toLowerCase().replace(/ /g, "-") in countries ?
            window.location.href = "/country/" + countries[country.trim().toLowerCase().replace(/ /g, "-")].toLowerCase() :
            Swal.fire({ title: 'Invalid Country Requested', icon: 'error', text: 'Please Try Again' });
    });
    $(".dcard").on("click", () => { window.location.href = "/all/deaths"; });
    $(".ccard").on("click", () => { window.location.href = "/all/confirmed"; });
    $(".rcard").on("click", () => { window.location.href = "/all/recovered"; });
});