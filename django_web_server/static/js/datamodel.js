function DataModel(urlRoot) {

	var that = this;

	that.princeEnquiryInfo = {
		"name" : "",
		"phone" : "",
		"email" : ""
	};

	// --------------------------------------------------
	// PROPERTY PROPERTY ACCESSORS

	that.udfSrc = function(property) {
		return urlRoot + 'data/udf/' + property.udf;
	};

	that.udfSrcForSelectedProperty = function() {
		
		return (that.selectedProperty !== null)
			? that.udfSrc(that.selectedProperty)
			: '';
	};

	that.summaryForStand = function(stand) {

		var s = "";

		if ((stand.name !== null) && (stand.name !== undefined) && (stand.name !== ''))
			s = s + stand.name + ': '

		if ((stand.areaSQM !== null)  && (stand.areaSQM !== 0)) {
			s = s + (stand.areaSQM / 10000).toFixed(2) + ' ha';
			s = s + ' (' + stand.areaSQM.toFixed(0) + ' sqm)';
		}			

		if (stand.units !== null)
			s = s + ' x ' + stand.units

		return s;
	};

	// --------------------------

	that.properties = [];

	that.selectedProperty = null;
	that.selectProperty = function(property) {
		that.selectedProperty = property;
	};

	that.categoryMatch = function(categoryName) {	
		return function( item ) {
			return item.category === categoryName;
		};
	};

	that.categoryViews = [
		{ category: "commercial", view: Views.COMMERCIAL },
		{ category: "industrial", view: Views.INDUSTRIAL },
		{ category: "residential", view: Views.RESIDENTIAL },
		{ category: "business", view: Views.BUSINESS },
		{ category: "hotel", view: Views.HOTEL },
		{ category: "retail", view: Views.RETAIL },
		{ category: "investment", view: Views.INVESTMENT },
		{ category: "sold", view: Views.SOLD },
	];

	that.viewForCategory = function(category) {
		for(var i = 0; i < that.categoryViews.length; i++)
			if (that.categoryViews[i].category == category)
				return that.categoryViews[i].view;
	};


	that.categoryForView = function(view) {
		for(var i = 0; i < that.categoryViews.length; i++)
			if (that.categoryViews[i].view == view)
				return that.categoryViews[i].category;
	};

	that.getPropertyCategoryViews = function() {
		var views = [];
		that.categoryViews.forEach(function(x){ views.push(x.view); });
		return views;
	};

	that.propertiesForCategory = function(category) {
		
		console.log('propertiesForCategory:  ', category);


		var matches = [];
		that.properties.forEach(function(p){
			if (p.category == category)
				matches.push(p);
		});

		console.dir(matches);

		return matches;
	};

	that.propertyNumberInCategory = function(property) {

		if ((property === undefined) || (property === null))
			return;

		return 1 + that.propertiesForCategory(property.category).indexOf(property);
	};

	that.shiftSelectedPropertyInCategory = function(shift) {
		if (that.selectedProperty == null)
			return;

		var category = that.selectedProperty.category;
		var properties = that.propertiesForCategory(category);

		var currentIndex =  properties.indexOf(that.selectedProperty);
		if (currentIndex == -1)
			return;

		var idx = currentIndex + shift;
		if (idx < 0)
			idx = idx + properties.length;
		if (idx >= properties.length)
			idx = idx - properties.length;

		that.selectedProperty = properties[idx];
	};

	that.selectPreviousPropertyInCategory = function() {
		that.shiftSelectedPropertyInCategory(-1);
	};
	that.selectNextPropertyInCategory = function() {
		that.shiftSelectedPropertyInCategory(1);
	};

}