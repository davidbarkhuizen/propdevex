function DataModel(siteUrlRoot) {

	var that = this;

	that.dataRootUrl = function() {
		return siteUrlRoot + 'data/';
	}

	that.url = function() {
		return that.dataRootUrl() + "datamodel.json";
	};

	that.dataImageUrl = function(imageFileName) {
		return that.dataRootUrl() + imageFileName;
	};

	// --------------------------------------------------
	// MODEL FIELDS

	that.categories = ["commercial","industrial","residential","business","hotel","retail","investment","agricultural"];

	that.categoryViews = [
		{ category: "commercial", view: Views.COMMERCIAL },
		{ category: "industrial", view: Views.INDUSTRIAL },
		{ category: "residential", view: Views.RESIDENTIAL },
		{ category: "business", view: Views.BUSINESS },
		{ category: "hotel", view: Views.HOTEL },
		{ category: "retail", view: Views.RETAIL },
		{ category: "investment", view: Views.INVESTMENT },
		{ category: "agricultural", view: Views.AGRICULTURAL },
		{ category: "sold", view: Views.SOLD },
	];

	that.contacts = [{
		"name" : "",
		"phone" : "",
		"email" : "",
		"categories" : []
	}];

	that.properties = [];

	// --------------------------------------------------
	// BIND MODEL

	var bound = false;
	
	that.isBound = function() {
		return bound;
	};

	that.bind = function(jsonResp) {

		// properties

		that.properties.length = 0;

		jsonResp.properties.forEach(function(property){
			that.properties.push(property);
		});

		// contacts

		that.contacts.length = 0;
		jsonResp.contacts.forEach(function(contact){
			that.contacts.push(contact);
		});

		bound = true;
	};

	// --------------------------------------------------
	// CATEGORIES

	that.categoryMatch = function(categoryName) {	
		return function( item ) {
			return item.category === categoryName;
		};
	};

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

	// --------------------------------------------------

	that.selectedCategory = null;
	that.selectCategory = function(category) {
		that.selectedCategory = category;
	};

	that.selectedProperty = null;
	that.selectProperty = function(property) {
		that.selectedProperty = property;
	};

	that.selectedSubProperty = null;
	that.selectSubProperty = function(subProperty) {
		that.selectedSubProperty = subProperty;
	};

	that.cancelSelection = function() {
		that.selectedCategory = null;
		that.selectedProperty = null;
		that.selectedSubProperty = null;
	};

	// --------------------------------------------------
	// PROPERTY PROPERTY ACCESSORS

	that.propertiesForCategory = function(category) {
		
		var matches = [];
		that.properties.forEach(function(p){
			if (p.category == category)
				matches.push(p);
		});

		return matches.reverse();
	};

	that.propertyHasArea = function(property) {

		if (property.areaSQM === null)
			return false;

		return true;
	};

	that.propertyAreaSqmText = function(property) {

		if (that.propertyHasArea(property) == false)
			return '';

		return property.areaSQM.toLocaleString() + ' sqm';
	};

	that.propertyAreaHaText = function(property) {

		if (that.propertyHasArea(property) == false)
			return '';

		return (property.areaSQM / 10000).toFixed(2) + ' ha';
	};

	that.propertyAreaText = function(property) {
		return that.propertyAreaHaText() + ' (' + that.propertyAreaSQMText() + ')';
	};

	/*

	that.imageSrc = function(imageFileName) {
		return urlRoot + 'data/' + imageFileName;
	};

	that.udfSrcForSelectedProperty = function() {
		
		return (that.selectedProperty !== null)
			? that.udfSrc(that.selectedProperty)
			: '';
	};

	that.standPropertyNumber = function(stand) {

		if ((stand === null) || (stand === undefined))
			return;

		var property = this.properties.first(function(p){

			return (p['stands'].indexOf(stand) !== -1); 
		});

		return property.stands.indexOf(stand) + 1;
	};

	that.standAreaText = function(stand) {
		
		if ((stand === null) || (stand === undefined))
			return '';

		var s = '';

		if ((stand.areaSQM !== null)  && (stand.areaSQM !== 0)) {
			s = s + (stand.areaSQM / 10000).toFixed(2) + ' ha';
			s = s + ' (' + stand.areaSQM.toFixed(0) + ' sqm)';
		}

		return s;
	};

	that.summaryForStand = function(stand) {

		var s = "";

		if ((stand.name !== null) && (stand.name !== undefined) && (stand.name !== ''))
			s = s + stand.name + ': '

		s = s + that.standAreaText(stand);

		if (stand.units !== null)
			s = s + ' x ' + stand.units

		return s;
	};

	*/

	// --------------------------

 

	/*

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

	// --------------------------------------------------

	that.shiftSelectedPropertyStand = function(shift) {
		
		if ((that.selectedProperty === undefined) || (that.selectedProperty === null))
			return;

		if ((that.selectedStand === undefined) || (that.selectedStand === null))
			return;

		var currentIndex = that.selectedProperty.stands.indexOf(that.selectedStand);
		if (currentIndex == -1)
			return;

		var idx = currentIndex + shift;
		if (idx < 0)
			idx = idx + that.selectedProperty['stands'].length;
		if (idx >= that.selectedProperty['stands'].length)
			idx = idx - that.selectedProperty['stands'].length;

		that.selectedStand = that.selectedProperty.stands[idx];
	};

	that.selectPreviousStandForProperty = function() {
		that.shiftSelectedPropertyStand(-1);
	};
	that.selectNextStandForProperty = function() {
		that.shiftSelectedPropertyStand(1);
	};

	*/
}