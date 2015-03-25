<?php
ini_set('display_errors', '1');
error_reporting(-1);
date_default_timezone_set('UTC');

require_once("ExchangeRateLoader.php");


$fullXchData = json_decode(str_replace(Array("ExchangeRateData = ", "}];"), Array("", "}]"), file_get_contents("../ExchangeRate-data.DB.days-7.js")));

$loader = new ExchangerateLoader();
$loader->loadJson($fullXchData);




$keys = $loader->getKeys();

if (isset($_GET['key']) && $_GET['key']) {
	$key = $_GET['key'];
}
else {
	#var_dump($keys);
	#exit();
	$key = end($keys);
}

#var_dump($loader->getDates());
#var_dump($loader->getUpdatesOnDate("2014-05-20"));
#var_dump($loader->getUpdatesOn("2014-05-20 16:50:00"));
#var_dump($loader->getCompleteUpdatesOn("2014-05-20 16:50:00"));
$xchData = $loader->getCompleteUpdatesOn($key);

$keyIdx = array_search($key, $keys);

$prevKey = null;
$nextKey = null;

if(isset($keys[$keyIdx-1])) {
	$prevKey = $keys[$keyIdx-1];
}
if(isset($keys[$keyIdx+1])) {
	$nextKey = $keys[$keyIdx+1];
}

$currency = 'EUR';
$toCurrency = 'RON';
			
uasort($xchData['sell'][$currency], function($a, $b) {
	$cmp = $a['value'] - $b['value'];
	if($cmp>0.000001) {
		return 1;
	}
	elseif($cmp<0.000001) {
		return -1;
	}
	else {
		return 0;
	}
});

#var_dump($xchData['sell'][$currency]);exit();

?>
<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, user-scalable=yes">
	
	<title>xCh - short info</title>
	<script>document.write('<base href="' + document.location + '" />');</script>
	<script src="//cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js"></script>
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
	<script src="//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min.js"></script>
	
	<!-- CSS -->
	<link rel="stylesheet" type="text/css" href="css/index.css" media="only screen and (min-device-width: 100px)" />
</head>

<body>
	<div class='stats'>
		<div>
			<span class='label'>recorded days</span>
			<span class='value'><?=count($loader->getDates())?></span>
		</div>
		
		<div>
			<span class='label'>recorded items</span>
			<span class='value'><?=count($loader->getKeys())?></span>
		</div>
	</div>
	
	<div class='lastXchData'>
		<div class='date'>
			<?php if($prevKey) { ?>
				<a class='goto prev'
					href="?key=<?=$prevKey?>">-</a>
			<?php } ?>
			
			<a class='reset' href="?key="><?=\DateTime::createFromFormat("Y-m-d H:i:s", $key)->format("d M, H:i")?></a>
			
			<?php if($nextKey) { ?>
				<a class='goto next'
					href="?key=<?=$nextKey?>">+</a>
			<?php } ?>
		</div>
		
		<div class='data'>
			<div class='currencyContainer <?=$currency?>'>
				<div class='currency'>
					<div class='label'>
						<input value="1" class="multiplier" type="number" step="any" />
						<span class='currency'><?=$currency?></span>
					</div>
					<div class='value' data-value="<?=$xchData['sell'][$currency]['BNR']['value']?>">
						<input value="<?=number_format($xchData['sell'][$currency]['BNR']['value'], 4)?>" class="multiplier" type="number" step="any" />
						<span class='currency'><?=$toCurrency?></span>
					</div>
				</div>
	
				<div class='banks'>
					<?php foreach($xchData['sell'][$currency] as $bank=>$data) { ?>
						<?php if ($bank!='BNR') { ?>
							<div class='bank-<?=$bank?> <?=($data['key']==$key?"value-changed-0":"")?>'>
								<span class='bank'><?=$bank?></span>
								<span class='value' data-value="<?=$data['value']?>"><?=number_format($data['value'], 4)?></span>
							</div>
						<?php } ?>
					<?php } ?>
				</div>
			</div>
		</div>
	</div>
	
	<script type="text/javascript">
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
	</script>
</body>
</html>
