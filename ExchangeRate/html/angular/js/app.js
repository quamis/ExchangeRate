var app = angular.module('ExchangeRate', ['n3-charts.linechart']);

app.controller('MainCtrl', function($scope) {
	$scope.data_EUR_sell = [];
	$scope.data_USD_sell = [];
	$scope.data_GBP_sell = [];
	
	
	var minDate = moment().subtract('weeks', 2).valueOf()
	
	for(k in ExchangeRateData){
		var data = ExchangeRateData[k];
		
		var dt = moment(data['date']).valueOf();
		
		if(dt>=minDate){
			$scope.data_EUR_sell.push({
				x: 					dt,
				BNR_sell: 			data['values']['BNR']['EUR']['sell'],
				RIB_sell: 			data['values']['RIB']['EUR']['sell'],
				AlphaBank_sell: 	data['values']['AlphaBank']['EUR']['sell'],
				BCR_sell: 			data['values']['BCR']['EUR']['sell'],
				
				RIB_buy: 			data['values']['RIB']['EUR']['buy'],
				AlphaBank_buy: 		data['values']['AlphaBank']['EUR']['buy'],
				BCR_buy: 			data['values']['BCR']['EUR']['buy'],
			});
			
			$scope.data_USD_sell.push({
				x: 					dt,
				BNR_sell: 			data['values']['BNR']['USD']['sell'],
				RIB_sell: 			data['values']['RIB']['USD']['sell'],
				AlphaBank_sell: 	data['values']['AlphaBank']['USD']['sell'],
				BCR_sell: 			data['values']['BCR']['USD']['sell'],
				
				RIB_buy: 			data['values']['RIB']['USD']['buy'],
				AlphaBank_buy: 		data['values']['AlphaBank']['USD']['buy'],
				BCR_buy: 			data['values']['BCR']['USD']['buy'],
			});
			
			$scope.data_GBP_sell.push({
				x: 					dt,
				BNR_sell: 			data['values']['BNR']['GBP']['sell'],
				RIB_sell: 			data['values']['RIB']['GBP']['sell'],
				AlphaBank_sell: 	data['values']['AlphaBank']['GBP']['sell'],
				BCR_sell: 			data['values']['BCR']['GBP']['sell'],
				
				RIB_buy: 			data['values']['RIB']['GBP']['buy'],
				AlphaBank_buy: 		data['values']['AlphaBank']['GBP']['buy'],
				BCR_buy: 			data['values']['BCR']['GBP']['buy'],
			});
		}
		
	}
	
	$scope.options_EUR_sell = {
		lineMode: 'linear', // monotone, cardinal, linear
		axes: {
			x: {
				type: 'date', 
				tooltipFormatter: function(x) {
					return moment(x).format('DD MMMM, HH:mm');
				}
			}
		},
		series: [
			{y: 'BNR_sell', 		color: '#ccc', label: 'BNR', type:'area' },
			{y: 'RIB_sell', 		color: '#800', label: 'RIB/sell', },
			{y: 'AlphaBank_sell', 	color: '#8c0', label: 'AlphaBank/sell', },
			{y: 'BCR_sell', 		color: '#88f', label: 'BCR/sell', },
			
			{y: 'RIB_buy', 			color: '#e66', label: 'RIB/buy', },
			{y: 'AlphaBank_buy', 	color: '#ae6', label: 'AlphaBank/buy', },
			{y: 'BCR_buy', 			color: '#ccf', label: 'BCR/buy', },
		]
	};
	
	$scope.options_USD_sell = $scope.options_EUR_sell;
	
	$scope.options_GBP_sell = $scope.options_EUR_sell;
});


app.controller('chart', function($scope) {

	/*$timeout(function() {
		$scope.minimized = 'minimized';
		console.info('a');
	}, 500);
	*/

	// $scope.minimized = 'minimized';
	
	$scope.toggleVisibility = function(element) {
		$scope.minimized = ($scope.minimized=='minimized'?'':'minimized');
	}
});
