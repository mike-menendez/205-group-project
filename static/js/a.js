// mapping of country to country code
const countries = {}
$("input").on("keypress", (country) =>{
    if('13' != (event.keyCode ? event.keyCode : event.which)){
        return
    }
    if(country.trim().toUpperCase().replace(/ /g,"") in countries){
        window.location.href="/country/" + c_code
    }
    else{
        Swal.fire({
            title: 'Invalid Country Requested',
            icon: 'error',
            text: 'Please Try again :)'
        })
    }
})