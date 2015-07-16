function DataModel() {

	var that = this;

	that.properties = [];

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
}