function treat_locale(locale) {
    return String(locale).replace('_', '-')
}

function format_currency(value, locale, currency) {
    return new Intl.NumberFormat(
        treat_locale(locale),
        {
            style: 'currency',
            currency: String(currency).toUpperCase()
        }
    ).format(value)
}

function format_date(date, locale) {
    return new Intl.DateTimeFormat(treat_locale(locale)).format(Date.parse(date))
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

function create_chart(el, type, labels, datasets) {
    return new Chart(el, {
        type: type,
        data: {
            labels: labels,
            datasets: datasets
        }
    })
}
