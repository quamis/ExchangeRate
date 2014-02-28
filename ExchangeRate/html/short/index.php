<?php

ini_set('display_errors', '1');
error_reporting(-1);

date_default_timezone_set('UTC');

$fullXchData = json_decode(str_replace(Array("ExchangeRateData = ", "}}}}};"), Array("", "}}}}}"), file_get_contents("../ExchangeRate-data.js")));

$stats = Array();
$stats['perDay'] = Array();
$stats['recordedItems'] = 0;

$lastData = null;
foreach($fullXchData as $k=>$xch) {
	$dt = DateTime::createFromFormat('Y-m-dH:i:sT', str_replace("T", "", $xch->date));
	
	if(!isset($stats['perDay'][$dt->format('Y-m-d')])) {
		$stats['perDay'][$dt->format('Y-m-d')] = Array();
		$stats['perDay'][$dt->format('Y-m-d')]['recordedItems'] = 0;
	}
	$stats['perDay'][$dt->format('Y-m-d')]['recordedItems']++;
	$stats['recordedItems']++;
	
	$lastXchData = $xch;
}

$lastXchData->date = DateTime::createFromFormat('Y-m-dH:i:sT', str_replace("T", "", $lastXchData->date));

$sortedSellXchData = Array();
foreach ($lastXchData->values as $bank=>$bxch) {
	foreach($bxch as $currency=>$xch) {
		if ($bank!='BNR') {
			$sortedSellXchData[$currency][$bank] = $xch->sell;
		}
	}
}



foreach($sortedSellXchData as $currency=>$x) {
	$v = $sortedSellXchData[$currency];
	asort($v);
	$sortedSellXchData[$currency] = $v;
}
$x = $sortedSellXchData;
$sortedSellXchData = Array();
foreach(Array('EUR', 'USD', 'GBP', 'CHF', ) as $k) {
	$sortedSellXchData[$k] = $x[$k];
	unset($x[$k]);
}
foreach($x as $k=>$v) {
	$sortedSellXchData[$k] = $x[$k];
	unset($x[$k]);
}


?>
<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, user-scalable=yes">
	
	<title>xCh - short info</title>
	<script>document.write('<base href="' + document.location + '" />');</script>
	<script src="lib/moment.js/moment.js"></script>
	
	<script src="lib/jquery/jquery.min.js"></script>
	<script src="lib/underscore.js/underscore.js"></script>
	
	<!-- CSS -->
	<link rel="stylesheet" type="text/css" href="css/index.css" media="only screen and (min-device-width: 100px)" />
</head>

<body>
	<div class='stats'>
		<div>
			<span class='label'>recorded days</span>
			<span class='value'><?=count($stats['perDay'])?></span>
		</div>
		
		<div>
			<span class='label'>recorded items</span>
			<span class='value'><?=$stats['recordedItems']?></span>
		</div>
	</div>
	
	<div class='lastXchData'>
		<div class='date'>
			<span class='value'><?=$lastXchData->date->format("d M, H:i");?></span>
		</div>
		
		<div class='data'>
			<?php foreach($sortedSellXchData as $currency=>$xchData) { ?>
				<div class='<?=$currency?>'>
					<div class='currency'>
						<div class='label'>
							<input value="1" class="multiplier" 
								onKeyup="
								var value = Number($(this).val());
								$(this).parents('div.currency').find('div.value').html(
									Number(value * $(this).parents('div.currency').find('div.value').attr('data-value')).toFixed(4)
								);
								
								$(this).parents('div.<?=$currency?>').find('div.banks span.value').each(function(i, sp) {
									$(sp).html(
										Number(value * $(sp).attr('data-value')).toFixed(4)
									);
								});
								" 
							/>
							<span onclick='switchCurrency();'><?=$currency?></span>
						</div>
						<div class='value' data-value="<?=$lastXchData->values->BNR->{$currency}->sell?>"><?=number_format($lastXchData->values->BNR->{$currency}->sell, 4)?></div>
					</div>
		
					<div class='banks'>
						<?php foreach($xchData as $bank=>$value) { ?>
							<div class='bank-<?=$bank?>'>
								<span class='bank'><?=$bank?></span>
								<span class='value' data-value="<?=$value?>"><?=number_format($value, 4)?></span>
							</div>
						<?php } ?>
					</div>
				</div>
			<?php } ?>
		</div>
	</div>
	
	<script type="text/javascript">
		function switchCurrency() {
			var elm = $('div.lastXchData>div.data>div.visible').get(0);
			if ($(elm).next().length) {
				$(elm).removeClass('visible').next().addClass('visible');
			}
			else {
				$(elm).removeClass('visible');
				$($(elm).siblings().get(0)).addClass('visible');
			}
		}
		$().ready(function() {
			$($('div.lastXchData>div.data>div').get(0)).addClass('visible');
		});
	</script>
</body>
</html>

