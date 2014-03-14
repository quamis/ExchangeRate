<?php

ini_set('display_errors', '1');
error_reporting(-1);

date_default_timezone_set('UTC');

$fullXchData = json_decode(str_replace(Array("ExchangeRateData = ", "}}}}};"), Array("", "}}}}}"), file_get_contents("../ExchangeRate-data.js")));

$stats = Array();
$stats['perDay'] = Array();
$stats['recordedItems'] = 0;

$lastXchData = null;
$prevKey = null;
$nextKey = null;
foreach($fullXchData as $k=>$xch) {
	$dt = DateTime::createFromFormat('Y-m-dH:i:sT', str_replace("T", "", $xch->date));
	
	if(!isset($stats['perDay'][$dt->format('Y-m-d')])) {
		$stats['perDay'][$dt->format('Y-m-d')] = Array();
		$stats['perDay'][$dt->format('Y-m-d')]['recordedItems'] = 0;
	}
	$stats['perDay'][$dt->format('Y-m-d')]['recordedItems']++;
	$stats['recordedItems']++;

	if (isset($_GET['id']) && $_GET['id']) {
		if ($_GET['id']==$k) {
			$lastXchData = $xch;
		}
		else {
			if ($lastXchData && $prevKey && !$nextKey) {
				$nextKey = $k;
			}
			
			if (!$lastXchData) {
				$prevKey = $k;
			}
		}
	}
	else {
		$lastXchData = $xch;
		
		$prevKey = $k;
	}
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
			<a class='goto prev'
				href="?id=<?=$prevKey?>">-</a>
			<span class='value'><?=$lastXchData->date->format("d M, H:i");?></span>
			<a class='goto next'
				href="?id=<?=$nextKey?>">+</a>
		</div>
		
		<div class='data'>
			<?php
			$currency = 'EUR';
			$toCurrency = 'RON';
			$xchData = $sortedSellXchData['EUR'];
			?>
			<div class='currencyContainer <?=$currency?>'>
				<div class='currency'>
					<div class='label'>
						<input value="1" class="multiplier" type="number" />
						<span class='currency'><?=$currency?></span>
					</div>
					<div class='value' data-value="<?=$lastXchData->values->BNR->{$currency}->sell?>">
						<input value="<?=number_format($lastXchData->values->BNR->{$currency}->sell, 4)?>" class="multiplier" type="number" />
						<span class='currency'><?=$toCurrency?></span>
					</div>
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
		</div>
	</div>
	
	<script type="text/javascript">
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
				var value = Number($(this).val());
				var BNRValue = Number($(this).parents('div.currency').find('div.value').attr('data-value'));
				var BNRValueFull = value * BNRValue;
				
				$(this).parents('div.currency').find('div.value>input').val(
					BNRValueFull.toFixed(4).replace(/0+$/, '')
				);
				
				recalcBankEquivalents($(this).parents('div.currencyContainer'), BNRValue, value);
			});
			
			$('div.value>input').on('keyup', function () {
				var value = Number($(this).val());
				
				
				var BNRValue = Number($(this).parents('div.currency').find('div.value').attr('data-value'));
				var BNRValueFull = value / BNRValue;
				
				$(this).parents('div.currency').find('div.label>input').val(
					BNRValueFull.toFixed(2)
				);
				
				recalcBankEquivalentsReverse($(this).parents('div.currencyContainer'), value, BNRValueFull);
			});
			
		});
	</script>
</body>
</html>

