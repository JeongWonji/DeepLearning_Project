function pushNotify(status, title, text, autoclose) {
    new Notify({
        status: status,
        title: title,
        text: text,
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: autoclose,
        autotimeout: 10000,
        gap: 40,
        distance: 20,
        type: 3,
        position: 'right bottom'
    })
}
//https://github.com/simple-notify/simple-notify