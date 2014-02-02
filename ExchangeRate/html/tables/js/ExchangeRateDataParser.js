function ExchangeRateDataParser(data){
	this.filters = { };
	this.data = $.map(data, function(elm){return elm}); // loose keys, keep it indexed by key
	
	this.reset();
}

ExchangeRateDataParser.prototype.destroy = function(){
}

ExchangeRateDataParser.prototype._next = function(){
	this.currentIndex++;
	var value = this.data[this.currentIndex];
	
	if(value==null)
		return null;
	
	var dt = moment.utc(value['date'], "YYYY-MM-DDTHH:mm:ssZ");
	
	if(this.filters['startDate'] && dt<this.filters['startDate']) {
		return 'row:skip';
	}

	if(this.filters['endDate'] && dt<this.filters['endDate']) {
		return 'row:skip';
	}
	
	return value;
}

ExchangeRateDataParser.prototype.next = function(){
	var value = null;
	do{
		value = this._next();
	}while(value==='row:skip');
	
	return value;
}

ExchangeRateDataParser.prototype.setFilter = function(key, value){
	this.filters[key] = value;
	return this;
}

ExchangeRateDataParser.prototype.addFilter = function(key, value){
	this.filters[key] = value;
	return this;
}


ExchangeRateDataParser.prototype.reset = function(){
	this.currentIndex = -1;
	this.rawData = [];
}

ExchangeRateDataParser.prototype.getRawData = function(){
	if(this.rawData.length==0) {
		var currentIndex = this.currentIndex;
		this.currentIndex = -1;
		do {
			var data = this.next();
			
			if(data) {
				this.rawData.push(data);
			}
		}while(data);
		this.currentIndex = currentIndex;
	}
	return this.rawData;
}

/*--------------------------------*/
ExchangeRateDataParser.prototype.nextWithCallback = function(callback){
	var data = this.next();
	if(data) {
		return callback(data);
	}
	return null;
}
