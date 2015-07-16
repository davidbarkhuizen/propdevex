function DataModel() {

	var that = this;

	that.properties = [];

	that.categoryMatch = function(categoryName) {	
		return function( item ) {
			return item.category === categoryName;
		};
	};
}