function _xCH(data){
	this.data = data;
	this.target = null;
	this.yesterdayValue = null;
	
	this.definedBanks = ['AlphaBank', 'CEC', 'RIB', 'Transilvania', 'BCR', ];
	this.referenceBank = 'BNR';
	this.CACHE = {};
}

_xCH.prototype.destroy = function(){
}

_xCH.prototype.reset = function(){
	this.data.reset();
	this.CACHE['data_parser_getMinMax'] = null;
	this.target.children().remove();
	return this;
}

_xCH.prototype.attach = function(target){
	this.target = target;
	return this;
}

_xCH.prototype.data_parser_getMinMax = function(currency){
	if(this.CACHE['data_parser_getMinMax']){
		return this.CACHE['data_parser_getMinMax'];
	}
	
	function _sorter(a, b) {
		return a-b;
	}
	
	function remap_extractBankData(bank, currency, operation, data) {
		try{
			return data['values'][bank][currency][operation];
		}catch(ex){
			return Math.NaN;
		}
	}
	
	var banks = this.definedBanks.slice(0);	// clone this.definedBanks
	banks.push(this.referenceBank);
	var ret = {};
	
	for(var i=0; i<banks.length; i++){
		var bank = banks[i];
		
		var values = this.data.getRawData().map(remap_extractBankData.bind(null, bank, 'EUR', 'sell')).filter(Number);
		
		ret[bank] = {};
		ret[bank]['sell'] = {};
		ret[bank]['sell']['min']  = Math.min.apply(Math, values);
		ret[bank]['sell']['max']  = Math.max.apply(Math, values);
		
		ret[bank]['sell']['min1p']  = ret[bank]['sell']['min'] + 0.01*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		ret[bank]['sell']['max1p']  = ret[bank]['sell']['max'] - 0.01*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		
		ret[bank]['sell']['min5p']  = ret[bank]['sell']['min'] + 0.05*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		ret[bank]['sell']['max5p']  = ret[bank]['sell']['max'] - 0.05*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		
		ret[bank]['sell']['min10p']  = ret[bank]['sell']['min'] + 0.1*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		ret[bank]['sell']['max10p']  = ret[bank]['sell']['max'] - 0.1*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		
		ret[bank]['sell']['min25p']  = ret[bank]['sell']['min'] + 0.25*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
		ret[bank]['sell']['max25p']  = ret[bank]['sell']['max'] - 0.25*(ret[bank]['sell']['max'] - ret[bank]['sell']['min']);
	}
	
	this.CACHE['data_parser_getMinMax'] = ret;
	return ret;
}

_xCH.prototype.data_parser_next = function(){
	var rawdata = this.data.next();
	var dt = {};
	
	if(!rawdata){
		return null;
	}
	dt['reference'] = 	Number(rawdata['values'][this.referenceBank]['EUR']['sell']);
	dt['date_raw'] = 	moment.utc(rawdata['date'], "YYYY-MM-DDTHH:mm:ssZ"); // date fmt: 2013-08-13T14:00:00+0000
	dt['date_ymd'] = 	dt['date_raw'].format("YYYY-MM-DD");
	dt['date'] = 		dt['date_raw'];
	
	dt['reference-diff'] = 0.0;
	if(this.yesterdayValue){
		dt['reference-diff'] = 		rawdata['values'][this.referenceBank]['EUR']['sell'] - this.yesterdayValue['values'][this.referenceBank]['EUR']['sell'];
		
		if(this.yesterdayValue['dt']['date_ymd']==dt['date_ymd']){
			dt['date'] = null;
		}
	}
	
	dt['banks'] = {};
	
	for(var i=0; i<this.definedBanks.length; i++){
		var bank = this.definedBanks[i];
		dt['banks'][bank] = {};
		dt['banks'][bank]['value'] = 0.0;
		dt['banks'][bank]['diff'] = 0.0;
		try{
			dt['banks'][bank]['value'] = rawdata['values'][bank]['EUR']['sell'];
			if(this.yesterdayValue){
				try{
					dt['banks'][bank]['diff'] = rawdata['values'][bank]['EUR']['sell'] - this.yesterdayValue['values'][bank]['EUR']['sell'];
				}catch(ex){
				}
			}
		}catch(ex){
		}
	}
	
	rawdata['dt'] = dt;
	
	this.yesterdayValue = rawdata;
	
	return dt;
}

_xCH.prototype.render_row_attachClasses = function(td, diff, value){
	var cls = 'diff-0000';
	if(Math.abs(diff)>1.000){
		cls = 'diff-1000';
	}else if(Math.abs(diff)>0.500){
		cls = 'diff-0500';
	}else if(Math.abs(diff)>0.250){
		cls = 'diff-0250';
	}else if(Math.abs(diff)>0.100){
		cls = 'diff-0100';
	}else if(Math.abs(diff)>0.050){
		cls = 'diff-0050';
	}else if(Math.abs(diff)>0.025){
		cls = 'diff-0025';
	}else if(Math.abs(diff)>0.010){
		cls = 'diff-0010';
	}else if(Math.abs(diff)>0.005){
		cls = 'diff-0005';
	}else if(Math.abs(diff)>0.002){
		cls = 'diff-0002';
	}else if(Math.abs(diff)>0.001){
		cls = 'diff-0001';
	}
	td.addClass(cls);
	

	var cls = 'variation-positive';
	if(diff>0){
		cls = 'variation-positive';
	}else if(diff==0){
		cls = 'variation-none';
	}else if(diff<0){
		cls = 'variation-negative';
	}
	td.addClass(cls);
}

function getWidth(dataTable, indexArr) {
	var width = 0;
	for(var i=0; i<indexArr.length; i++) {
		if(indexArr[i]==0) {
			width+= $($(dataTable).find('>tbody>tr:first>td').get(indexArr[i])).outerWidth(true);
		}
		else if(indexArr[i]>3) {
			if(indexArr[i]%2==0) {
				width+= $($(dataTable).find('>tbody>tr:first>td').get(indexArr[i])).outerWidth(true)-1;
			}
			else {
				width+= $($(dataTable).find('>tbody>tr:first>td').get(indexArr[i])).width();
			}
		}
		else {
			width+= $($(dataTable).find('>tbody>tr:first>td').get(indexArr[i])).width();
		}
	}
	
	return width;
}
	
_xCH.prototype._add_header = function(trh, dataTable){
	
	trh.append($('<td colspan="2">').html("date").width(getWidth(dataTable,[0,1])) );
	trh.append($('<td>').html("hour").width(getWidth(dataTable, [2])));
	
	trh.append($('<td colspan="2">').html("BNR").width(getWidth(dataTable,[3,4])));
	
	for(var i=0; i<this.definedBanks.length; i++){
		trh.append($('<td colspan="2">').html(this.definedBanks[i]).width(getWidth(dataTable,[i*2+5, i*2+5+1])) );
	}
	
	return trh;
}


_xCH.prototype.render_row = function(tr, dt){
	if(dt['date']){
		tr.addClass('newDay');
		tr.append($('<td>').addClass('dayOfWeek').html( dt['date'].format("ddd") ));
		tr.append($('<td>').addClass('date').html( dt['date'].format("MMM Do") ));
		tr.append($('<td>').addClass('hour').html( dt['date_raw'].format("HH:mm") ));
	} else {
		tr.append($('<td>').addClass('dayOfWeek').html( '' ));
		tr.append($('<td>').addClass('date').html( '' ));
		tr.append($('<td>').addClass('hour').html( dt['date_raw'].format("HH:mm") ));
	}
	
	var diff = dt['reference-diff'];
	var value = dt['reference'];
	
	var min_max = this.data_parser_getMinMax();
	
	var td;
	td = $('<td>').addClass('reference').addClass('value').html(value.toFixed(4));
	this.render_row_attachClasses(td, diff, value);
	tr.append(td);
	
	td = $('<td>').addClass('reference').addClass('diff').html( (diff>=0?'+':'') + Number(diff).toFixed(4) );
	tr.append(td);
	
	for(var bank in dt['banks']){
		value = dt['banks'][bank]['value'];
		diff = dt['banks'][bank]['diff'];
		
		if(value!=0.0){
			td = $('<td>').addClass('bank-'+bank).addClass('value').html( value.toFixed(4) );
			this.render_row_attachClasses(td, diff, value);
			if(value<min_max[bank]['sell']['min1p']) {
				td.addClass('minimum-01p');
			}else if(value<min_max[bank]['sell']['min5p']) {
				td.addClass('minimum-05p');
			}else if(value<min_max[bank]['sell']['min10p']) {
				td.addClass('minimum-10p');
			}else if(value<min_max[bank]['sell']['min25p']) {
				td.addClass('minimum-25p');
			}
			
			if(value>min_max[bank]['sell']['max1p']) {
				td.addClass('maximum-01p');
			}else if(value>min_max[bank]['sell']['max5p']) {
				td.addClass('maximum-05p');
			}else if(value>min_max[bank]['sell']['max10p']) {
				td.addClass('maximum-10p');
			}else if(value>min_max[bank]['sell']['max25p']) {
				td.addClass('maximum-25p');
			}
			
			tr.append(td);
			
			td = $('<td>').addClass('bank-'+bank).addClass('diff').html( (diff>=0?'+':'') + Number(diff).toFixed(4) );
			this.render_row_attachClasses(td, diff, diff);
			tr.append(td);
		} else {
			td = $('<td>').addClass('bank-'+bank).addClass('value').html( '-' );
			tr.append(td);
			
			td = $('<td>').addClass('bank-'+bank).addClass('diff').html( '-' );
			tr.append(td);
		}
	}
	
	return tr;
}



_xCH.prototype.render_header = function(dataTable){
	var tableHeader = $('<table>');
	this.target.append(tableHeader);
	tableHeader.addClass('header');
	var trh = $('<tr>');
	trh = this._add_header(trh, dataTable);
	tableHeader.append(trh);
	
	return this;
}


_xCH.prototype.render = function(){
	var table = $('<table>');
	
	this.target.append(table);
	
	table.addClass('data');

	var lastValue = null;
	while(dt = this.data_parser_next()){
		var tr = $('<tr>');
		tr = this.render_row(tr, dt);
		
		if(tr.hasClass('newDay')) {
			tbody = $('<tbody>');
			tbody.addClass('day');
			table.append(tbody);
		}
		tbody.append(tr);
	}
	
	this.render_header(table);
	
	return this;
}
