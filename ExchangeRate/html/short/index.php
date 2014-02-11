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
	<title>xCh - short info</title>
	<script>document.write('<base href="' + document.location + '" />');</script>
	<script src="lib/moment.js/moment.js"></script>
	
	<script src="lib/jquery/jquery.min.js"></script>
	<script src="lib/underscore.js/underscore.js"></script>
	
	<!-- CSS -->
	<link rel="stylesheet" href="css/index.css">
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
		<div>
			<span class='label'>date</span>
			<span class='value'><?=$lastXchData->date->format("d M, H:i");?></span>
		</div>
		
		<div>
			<?php foreach($sortedSellXchData as $currency=>$xchData) { ?>
				<div class='data <?=$currency?>'>
					<span class='label'><?=$currency?></span>
					<span class='value'><?=number_format($lastXchData->values->BNR->{$currency}->sell, 4)?></span>
			
					<div class='banks'>
						<?php foreach($xchData as $bank=>$value) { ?>
							<span class='label'><?=$bank?></span>
							<span class='value'><?=number_format($value, 4)?></span>
						<?php } ?>
					</div>
				</div>
			<?php } ?>
		</div>
	</div>
</body>
</html>

