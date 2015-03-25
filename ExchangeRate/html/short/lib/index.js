evalEq = function(text) {
	if (text.match(/[^0-9\.\/\+\*\-]/)) {
		return 0;
	}
	
	return new Function("", "return Number("+text+");")();
}

recalcBankEquivalents = function (parent, BNRValue, value) {
	var BNRValueFull = value * BNRValue;

	$(parent).find('div.banks span.value').each(function(i, sp) {
		var valueFull = value * Number($(sp).attr('data-value'));
		$(sp).html( ""
			+ "<span class='recalculated'>" + valueFull.toFixed(2) + "</span>"
			+ "<span class='BNRDiff'>+" + (valueFull - BNRValueFull).toFixed(2) + "</span>"
		);
	});
}

recalcBankEquivalentsReverse = function (parent, value, BNRValueFull) {
	$(parent).find('div.banks span.value').each(function(i, sp) {
		var valueFull = value / Number($(sp).attr('data-value'));
		$(sp).html( ""
			+ "<span class='recalculated'>" + valueFull.toFixed(2) + "</span>"
			+ "<span class='BNRDiff'>+" + (BNRValueFull - valueFull).toFixed(2) + "</span>"
		);
	});
}

$().ready(function() {
	$('input.multiplier').on('focus', function () {
		$(this).select();
	});
	
	$('div.label>input').on('keyup', function () {
		var value = evalEq($(this).val());
		var BNRValue = Number($(this).parents('div.currency').find('div.value').attr('data-value'));
		
		var BNRValueFull = value * BNRValue;
		
		$(this).parents('div.currency').find('div.value>input').val(
			BNRValueFull.toFixed(4).replace(/(\.)?[0]+$/, '')
		);
		
		recalcBankEquivalents($(this).parents('div.currencyContainer'), BNRValue, value);
	});
	
	$('div.value>input').on('keyup', function () {
		var value = evalEq($(this).val());
		
		
		var BNRValue = Number($(this).parents('div.currency').find('div.value').attr('data-value'));
		var BNRValueFull = value / BNRValue;
		
		$(this).parents('div.currency').find('div.label>input').val(
			BNRValueFull.toFixed(2)
		);
		
		recalcBankEquivalentsReverse($(this).parents('div.currencyContainer'), value, BNRValueFull);
	});
	
});