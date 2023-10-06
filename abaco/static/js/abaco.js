function format_currency(value, locale, currency) {
    return new Intl.NumberFormat(
        String(locale).replace('_', '-'),
        {
            style: 'currency',
            currency: String(currency).toUpperCase()
        }
    ).format(value)
}

function ajax_requester(url, data = null, method = 'POST', reload = true, success_callback = null) {
    $.ajax({
        method: method,
        url: url,
        data: data,
        dataType: "json",
        encode: true,
        contentType: 'application/json'
    }).done(function (data) {
        if (data.message) {
            alert(data.message)
        }
        if (success_callback != null) {
            success_callback.forEach(function (func) {
                func(data)
            })
        }
        if (reload) {
            location.reload()
        }
    }).fail((response) => {
        alert('Error: ' + response.responseJSON.message)
    })
}
