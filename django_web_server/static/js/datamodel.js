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

	that.categories = ["commercial","industrial","residential","business","hospitality","retail","investment","agricultural"];

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

	// --------------------------------------------------

	that.selectedCategory = null;
	that.selectCategory = function(category) {
		that.selectedCategory = category;
	};

	that.selectedProperty = null;
	that.selectProperty = function(property) {
		that.selectedProperty = property;
		that.selectedPropertyImageIndex = 0;

		if (property.sold == false) {
			that.selectCategory(property.category);
		}
		else {
			if (that.selectedCategory !== 'sold')
				that.selectedCategory = 'sold';
		}
	};

	that.selectNextPropertyInCategory = function() {

		var properties = that.propertiesForCategory(that.selectedCategory);

		if ((properties.length == 0) || (properties.length == 1))
			return;

		var index = properties.indexOf(that.selectedProperty);
		index = index + 1;
		if (index === properties.length)
			index = 0;

		that.selectProperty(properties[index]); 
	};

	that.selectPreviousPropertyInCategory = function() {

		var properties = that.propertiesForCategory(that.selectedCategory);

		if ((properties.length === 0) || (properties.length === 1)){
			return;
		}

		var index = properties.indexOf(that.selectedProperty);
		index = index - 1;
		if (index === -1) {
			index = properties.length - 1;
		}

		that.selectProperty(properties[index]); 
	};

	that.selectedSubProperty = null;
	that.selectSubProperty = function(subProperty) {
		that.selectedSubProperty = subProperty;
	};

	that.selectedPropertyImageIndex = 0;
	that.getSelectedPropertyImage = function() {

		if ((that.selectedProperty === null) || (that.selectedProperty.images.length == 0))
			return null;

		return that.selectedProperty.images[that.selectedPropertyImageIndex];
	};

	that.selectNextPropertyImage = function() {

		that.selectedPropertyImageIndex = that.selectedPropertyImageIndex + 1;
		if (that.selectedPropertyImageIndex >= that.selectedProperty.images.length)
			that.selectedPropertyImageIndex = 0;
	};

	that.selectPreviousPropertyImage = function() {

		that.selectedPropertyImageIndex = that.selectedPropertyImageIndex - 1;
		if (that.selectedPropertyImageIndex < 0)
			that.selectedPropertyImageIndex = that.selectedProperty.images.length - 1;
	};

	that.cancelSelection = function() {
		that.selectedCategory = null;
		that.selectedProperty = null;
		that.selectedPropertyImageIndex = 0;
		that.selectedSubProperty = null;
	};

	// --------------------------------------------------
	// CONTACT PROPERTY ACCESSORS

	that.contactsForCategory = function(category) {

		var contactsForCategory = [];
		that.contacts.forEach(function(contact){
			if (contact.categories.indexOf(category) !== -1) {
				contactsForCategory.push(contact);
			}
		});

		if (contactsForCategory.length == 0) {
			contactsForCategory.push(that.contacts[0]);
		}

		return contactsForCategory;
	}

	// --------------------------------------------------
	// PROPERTY PROPERTY ACCESSORS

	that.propertiesForCategory = function(category) {
		
		var matches = [];

		if (category !== 'sold'){
			that.properties.forEach(function(p){
				if ((p.category == category) && (p.sold == false))
					matches.push(p);
			});
		} else {
			that.properties.forEach(function(p){
				if (p.sold == true)
					matches.push(p);
			});
		}

		return matches;
	};

	// PROPERTIES - PAGING

	that.propertiesPerPage = 6;
	that.propertiesPageNumber = 1;

	that.setPropertiesPageNumber = function(num) {
		that.propertiesPageNumber = num;
	};
	
	that.propertiesForCategoryPageNumbers = function(category) {
		var numbers = [];
		var count = that.propertiesForCategoryPageCount(category);
		for (var i = 0; i < count; i++) {
			numbers.push(i + 1);
		}

		return numbers;
	};

	that.propertiesForCategoryPageCount = function(category) {

		var itemCount = that.propertiesForCategory(category).length;

		var pageCount = Math.floor(itemCount / that.propertiesPerPage);

		if (itemCount % that.propertiesPerPage !== 0)
			pageCount = pageCount + 1;

		return pageCount;
	};

	that.propertiesForCategoryPaged = function(category) {
		
		var all = that.propertiesForCategory(category);

		var start = (that.propertiesPageNumber - 1) * that.propertiesPerPage;

		var page = [];
		for (var i = start; (i < start + that.propertiesPerPage) && (i < all.length); i++)
			page.push(all[i]);

		return page;
	};


	that.propertyHasArea = function(property) {

		if ((property == null) || (property.areaSQM === null))
			return false;

		return true;
	};

	that.propertyAreaSqmText = function(property) {

		if (that.propertyHasArea(property) == false)
			return '';

		return property.areaSQM.toLocaleString() + ' m²';
	};

	that.propertyAreaHaText = function(property) {

		if ((property === null) || (property == undefined))
			return '';

		if (that.propertyHasArea(property) == false)
			return '';

		return (property.areaSQM / 10000).toFixed(2) + ' ha';
	};

	that.propertyAreaText = function(property) {
		return that.propertyAreaHaText() + ' (' + that.propertyAreaSQMText() + ')';
	};

	that.geoLocURL = function(property) {

		var latStr = property.latitude.toFixed(4);

		if (property.latitude < 0)
			latStr = '-' + latStr;
		else		
			latStr = '+' + latStr;

		var lonStr = property.longitude.toFixed(4);

		if (property.longitude < 0)
			lonStr = '-' + lonStr;
		else		
			lonStr = '+' + lonStr;

		var s = latStr + lonStr;
		var url = 'http://maps.google.com/maps?z=12&t=k&q=loc:' + s;

		return url;
	};

	that.propertyHasGPSCoOrdinates = function(property) {

		if (property === null)
			return false;

		var lat = parseFloat(property.latitude);
		var lon = parseFloat(property.longitude);

		if (isNaN(lat) || isNaN(lon))
			return false;

		return true;
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