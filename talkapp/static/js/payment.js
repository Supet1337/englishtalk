function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}

var widget = new cp.CloudPayments();
function pay(amount) {
    widget.pay('auth', // или 'charge'
        { //options
            publicId: 'pk_88cbc6ba5f4e2c1ab61f1bfb76b49', //id из личного кабинета
            description: 'Оплата уроков в eng-talk.ru', //назначение
            amount: amount, //сумма
            currency: 'RUB', //валюта
            accountId: 'user@example.com', //идентификатор плательщика (необязательно)
            skin: "classic", //дизайн виджета (необязательно)
            retryPayment: true,
            data: {
                myProp: 'myProp value'
            }
        },
        {
            onSuccess: function (options) {
				$.ajax({
					type: "POST",
					url: "ajax_pay_lessons",
					data: {
						csrfmiddlewaretoken: getCookie('csrftoken'),
						cost: options.amount
					},
				})
			},
            onFail: function (reason, options) { // fail
                widget = new cp.CloudPayments();
            },
            onComplete: function (paymentResult, options) { //Вызывается как только виджет получает от api.cloudpayments ответ с результатом транзакции.
                //например вызов вашей аналитики Facebook Pixel
            }
        }
    )
};
$('button[id^="pay-"]').click(function () {
	i = $(this).attr("id");
	const amount = i.slice(4);
	pay(parseInt(amount));
})