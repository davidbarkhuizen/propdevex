function GodController($rootScope, $scope, $http, $timeout, $interval) {

	var siteRoot = '/static/';

	// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	// DATA MODEL 

	$scope.model = new DataModel(siteRoot);

	$scope.loadDataModel = function() {

		var request = 
		{
			method: 'GET',
			url: suffixStaticUrlWithGuid($scope.model.url()),
		};

		function handleSuccess(response) { 

			$scope.model.bind(response);
		};

		function handleError(response) { 

			// TODO = explode visibly - i.e. with red error
			console.log(response);
		};

		$http(request)
			.success(handleSuccess)
			.error(handleError);
	};	

	// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	// VIEWS	

	$scope.Views = Views;
	$scope.view = Views.HOME;

	$scope.showView= function(view) {
		return ($scope.view === view);
	};

	$scope.gotoHomeView = function() {
		$scope.model.cancelSelection();
		$scope.view = Views.HOME; 
	};

	$scope.gotoCategoryView = function(category) {

		if (category === undefined)
			category = $scope.model.categories[0];

		$scope.model.cancelSelection();
		$scope.model.selectCategory(category);

		$scope.view = Views.CATEGORY; 
	};

	$scope.viewProperty = function(property) {
		$scope.view = Views.PROPERTY;
		$scope.model.selectProperty(property);
	}

	$scope.gotoSoldView = function() {
		$scope.model.cancelSelection();
		$scope.view = Views.SOLD; 
	};

	$rootScope.$on(Command.GOTO_VIEW, function(evt, view) { 

		switch(view) {
			case Views.HOME:
				$scope.gotoHomeView();
				break;
			case Views.CATEGORY:
				$scope.gotoCategoryView();
				break;
			case Views.SOLD:
				$scope.gotoSoldView();
				break;
		}
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

	$scope.mailToHref = function(toAddr, subject) {
		return 'mailto:' + toAddr + '?Subject=' + encodeURIComponent(subject);
	};

	$scope.enquireAfterPriceOfSelectedProperty = function() {

		var category = $scope.model.selectedProperty['category'];

		var contactsForCategory = [];
		$scope.model.contacts.forEach(function(contact){
			if (contact.categories.indexOf(category) !== -1) {
				contactsForCategory.push(contact);
			}
		});

		if (contactsForCategory.length == 0) {
			contactsForCategory.push($scope.model.contacts[0]);
		}

		var href = $scope.mailToHref(contactsForCategory[0]['email'], $scope.model.selectedProperty['name']);
		window.open(href, '_blank');
	};

	$scope.viewStandDetail = function(stand) {
		$scope.model.selectStand(stand);
		$scope.modalController.openModal();
	};

	// -----------------------------------------------------------------
	/* SOCIAL LINKS */

	$scope.openUrlInNewWindow = function(url) {
		window.open(url, '_blank');
	}

	$scope.openFacebook = function() {
		$scope.openUrlInNewWindow('https://www.facebook.com');
	};

	$scope.openTwitter = function() {
		$scope.openUrlInNewWindow('https://www.twitter.com');
	};

	$scope.openLinkedIn = function() {
		$scope.openUrlInNewWindow('https://www.linkedin.com');
	};

	// -----------------------------------------------------------------
	/* TWITTER WIDGET */

	$scope.init_twitter_widget = function() {
        		
		var
			s = "script",
			id = "twitter-wjs";

		var js,
			fjs = document.getElementsByTagName(s)[0],
			p = /^http:/.test(document.location)
				? 'http'
				: 'https';

		if (!document.getElementById(id)) {
			js = document.createElement(s);
			js.id = id;
			js.src = p + "://platform.twitter.com/widgets.js";
			fjs.parentNode.insertBefore(js,fjs);
		}
	};

	/* ------------------------------------------ */
	/* HOME VIEW */

	$scope.homeImageSrcs = [
		'/static/image/slide01_sized.jpg',
		'/static/image/slide02_sized.jpg',
		'/static/image/slide03.jpg'
	];

	$scope.homeImageSrcIndex = 0;

	$scope.homeImageSrc = function() {
		return $scope.homeImageSrcs[$scope.homeImageSrcIndex];
	};
	
	$scope.rotateHomeImageSrcIndex = function() {
		
		$scope.homeImageSrcIndex = $scope.homeImageSrcIndex + 1;
		
		if ($scope.homeImageSrcIndex >= $scope.homeImageSrcs.length)
			$scope.homeImageSrcIndex = 0;
	};

	$interval($scope.rotateHomeImageSrcIndex, 5000);

	// -----------------------------------------------------------------
	// INIT

	$scope.loadDataModel();
	$timeout($scope.init_twitter_widget, 500);
};