function ExchangeRateDataParser(data){
	this.filters = { };
	this.reset();
	
	var x = this.remap(data);
	this.groupedData = x.groupedData;
	this.definedBanks = x.definedBanks;
	this.definedCurrencies = x.definedCurrencies;
	
	
}

ExchangeRateDataParser.prototype.reset = function(){
	this.currentIndex = -1;
	this.groupedData = [];
	this.definedBanks = [];
	this.definedCurrencies = [];
}

ExchangeRateDataParser.prototype.destroy = function(){
}

ExchangeRateDataParser.prototype.remap = function(data){
	var definedCurrencies = {};
	var definedBanks = {};

	var gdata = {};
	for(var i=0; i<data.length; i++) {
		var xch = data[i];
		var ymd = 		xch['time'].substring(0, 10);
		var ymdhis = 	xch['time'].substring(0, 10) + " " + xch['time'].substring(11);
		
		if (definedCurrencies[xch['currency']]==null) {
			definedCurrencies[xch['currency']] = 0;
		}
		definedCurrencies[xch['currency']]++;
		
		if (definedBanks[xch['bank']]==null) {
			definedBanks[xch['bank']] = 0;
		}
		definedBanks[xch['bank']]++;
		
		
		if (gdata[ymdhis]==null) {
			gdata[ymdhis] = {};
		}
		if (gdata[ymdhis][xch['type']]==null) {
			gdata[ymdhis][xch['type']] = {};
		}
		if (gdata[ymdhis][xch['type']][xch['currency']]==null) {
			gdata[ymdhis][xch['type']][xch['currency']] = {};
		}
		if (gdata[ymdhis][xch['type']][xch['currency']][xch['bank']]==null) {
			gdata[ymdhis][xch['type']][xch['currency']][xch['bank']] = {};
		}
		
		gdata[ymdhis][xch['type']][xch['currency']][xch['bank']] = xch['value'];
	}
	
	return {
		'groupedData': gdata,
		'definedBanks': _.keys(definedBanks),
		'definedCurrencies': _.keys(definedCurrencies),
	};
}

ExchangeRateDataParser.prototype.getRawGroupedData = function(){
	return this.groupedData ;
}


ExchangeRateDataParser.prototype.getKeys = function(){
	return _.keys(this.groupedData) ;
}

ExchangeRateDataParser.prototype.getDates = function(){
	return _.uniq(this.getKeys().map(function(a){ return a.substr(0, 10); })).sort();
}

ExchangeRateDataParser.prototype.getUpdatesOnDate = function(dt){
	return _.pick(this.getRawGroupedData(), this.getKeys().filter(function(a){ return a.substr(0, 10)==dt;}))
}

ExchangeRateDataParser.prototype.getUpdatesOn = function(dtt){
	return this.getRawGroupedData()[dtt];
}

ExchangeRateDataParser.prototype.getCompleteUpdatesOn = function(dtt){
	var root = this.groupedData[dtt];
	var ret = {};
	var gatheredCurrencies = {};
	var gatheredBanks = {};
	
	for(var operation in root) {
		for(var currency in root[operation]) {
			for(var bank in root[operation][currency]) {
				if (ret[operation]==null) {
					ret[operation] = {};
				}
				if (ret[operation][currency]==null) {
					ret[operation][currency] = {};
				}
				if (ret[operation][currency][bank]==null) {
					ret[operation][currency][bank] = {};
				}
				
				ret[operation][currency][bank] = {
					'value':	root[operation][currency][bank], 
					'key':		dtt,
				};
				
				if(gatheredCurrencies[currency]==null) {
					gatheredCurrencies[currency] = 0;
				}
				gatheredCurrencies[currency]++;
				
				if(gatheredBanks[bank]==null) {
					gatheredBanks[bank] = 0;
				}
				if(gatheredBanks[bank][currency]==null) {
					gatheredBanks[bank][currency] = 0;
				}
				gatheredBanks[bank][currency]++;
			}
		}
	}
	
	var keys = this.getKeys();
	var keyIdx = keys.indexOf(dtt);
	
	var brk = false;
	for(var idx=keyIdx; idx>0; idx--) {
		var key = keys[idx];
		var data = this.groupedData[key];
		
		for(var operation in data) {
			for(var currency in data[operation]) {
				for(var bank in data[operation][currency]) {
					if (ret[operation]==null) {
						ret[operation] = {};
					}
					if (ret[operation][currency]==null) {
						ret[operation][currency] = {};
					}
					if (ret[operation][currency][bank]==null) {
						ret[operation][currency][bank] = {};
					}
					
					if(ret[operation][currency][bank]['value']==null) {
						ret[operation][currency][bank] = {
							'value':	data[operation][currency][bank], 
							'key':		key,
						};
					}
					
					if(gatheredCurrencies[currency]==null) {
						gatheredCurrencies[currency] = 0;
					}
					gatheredCurrencies[currency]++;
					
					if(gatheredBanks[bank]==null) {
						gatheredBanks[bank] = 0;
					}
					if(gatheredBanks[bank][currency]==null) {
						gatheredBanks[bank][currency] = 0;
					}
					gatheredBanks[bank][currency]++;
				}
			}
		}
		
		if(_.keys(gatheredCurrencies).length==this.definedCurrencies.length && _.keys(gatheredBanks).length==this.definedBanks.length) {
			var allFound = true;
			for(var b in gatheredBanks) {
				if (gatheredBanks[b].length!=this.definedBanks.length) {
					allFound = false;
					break;
				}
			}
			
			if (allFound) {
				brk = true;
				break;
			}
		}
	}
	
	return ret;
}
