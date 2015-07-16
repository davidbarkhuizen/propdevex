function GodController($rootScope, $scope, $http, $timeout) {

	$scope.model = new DataModel('/static/');

	// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	// VIEWS	

	$scope.nlIsActive = function(view) {
		
		if ($scope.view === view)
			return true;

		if ($scope.view === Views.PROPERTY) {
			return ($scope.model.categoryForView(view) == $scope.model.selectedProperty.category)
		}

		return false;
	}

	$scope.Views = Views;
	$scope.view = Views.HOME;

	$scope.showView= function(view) {
		return ($scope.view === view);
	};

	$scope.gotoView = function(newView) {
		$scope.view = newView;	
	
		var bindWindow = function () {

			// focus on element marked with data-focus-element attribute 
			// 
			$scope.giveActiveViewFocus();

			// ui-grids only display correctly after this event if
			// initially rendered off-screen
			//
			//var evt = document.createEvent('HTMLEvents');
			//evt.initEvent('resize', true, false);
			//window.dispatchEvent(evt);
		};

		$timeout(bindWindow, 100);
	};

	$rootScope.$on(Command.GOTO_VIEW, function(evt, view) { 
		$scope.gotoView(view);
	});

	$rootScope.$on(Event.DEBUG_ERROR, function(evt, error) {
		$scope.globalDebug(error);
	});

	$scope.giveActiveViewFocus = function() {
		
		// data-focus-element

		var views = document
			.getElementById('viewport')
			.childNodes;

		for(var i = 0; i < views.length; i++) {

			var className = views[i].className;

			if (className !== undefined) {
				if ((' ' + className + ' ').indexOf(' ' + 'ng-hide' + ' ') == -1) {

					var q =  '[' + 'data-focus-element' + ']';
					var focusElement = views[i].querySelector(q);
					if (focusElement)
						focusElement.focus();
				}
			}
		}
	};

	// WINDOW / LAYOUT ----------------------------------------

	$scope.getWindowDimensions = function() {

		var navbar = document.getElementById('navbar');
		var fudge = navbar.parentNode.offsetHeight + 10;

		var dims = {
			height : window.innerHeight - fudge, 
			width : document.body.offsetWidth
		};

		return dims;
	};

	// -----------------------------------------------------------------
	// LOAD DATA MODEL

	$scope.loadDataModel = function() {

		var request = 
		{
			method: 'GET',
			url: "/static/data/datamodel.json",
		};

		function handleSuccess(response) { 

			// load properties
			//
			response.properties.forEach(function(x){
				$scope.model.properties.push(x);
			});

			$scope.model.princeEnquiryInfo = response.princeEnquiryInfo;
		};

		function handleError(response) { 

			console.log(response);
		};

		$http(request)
			.success(handleSuccess)
			.error(handleError);
	};

	// -----------------------------------------------------------------

	$scope.viewProperty = function(property) {
		$scope.model.selectProperty(property);
		$scope.gotoView(Views.PROPERTY);
	}

	// -----------------------------------------------------------------

	$scope.mailToHref = function(toAddr, subject) {
		return 'mailto:' + toAddr + '?Subject=' + encodeURIComponent(subject);
	};

	$scope.enquireAfterPriceOfSelectedProperty = function() {

		var href = $scope.mailToHref($scope.model.princeEnquiryInfo['email'], $scope.model.selectedProperty['name']);
		console.log(href);

		window.open(href, '_blank');
	};

	// -----------------------------------------------------------------
	// INIT

	$scope.loadDataModel();
};