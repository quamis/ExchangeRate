<?php
$fullData = json_decode(str_replace(Array("ExchangeRateData = ", "}}}}};"), Array("", "}}}}}"), file_get_contents("../ExchangeRate-data.js")));

$stats = Array();

$lastData = null;
foreach($fullData as $k=>$data) {
	$dt = DateTime::createFromFormat('Y-m-dH:i:sT', str_replace("T", "", $data->date));
	$stats['perDay'][$dt->format('Y-m-d')]['recordedItems']++;
	$stats['recordedItems']++;
	
	$lastData = $data;
}

$lastData->date = DateTime::createFromFormat('Y-m-dH:i:sT', str_replace("T", "", $lastData->date));
var_dump($lastData);

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
	
	<div class='lastData'>
		<div>
			<span class='label'>date</span>
			<span class='value'><?=$lastData->date->format("d M, H:i")?></span>
		</div>
		
		<div>
			<span class='label'>EUR</span>
			<span class='value'><?=number_format($lastData->values->BNR->EUR->sell, 4)?></span>
		</div>
	</div>
</body>
</html>

