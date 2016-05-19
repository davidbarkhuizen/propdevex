var Command = Object.freeze({
	GOTO_VIEW : guid()
});

function GodController($rootScope, $scope, $http, $timeout, $interval) {

	var siteRoot = '/static/';

	// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

	$scope.deUnderscore = function (underscored) {

		if ((underscored === undefined) || (underscored === null))
			return ''; 

		return underscored
			.split('_')
			.map(function(w){ return w[0].toUpperCase() + w.substring(1); })
			.join(' ');
	};

	// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
	// DATA MODEL 

	$scope.model = new DataModel(siteRoot);

	$scope.decodeURI = function(encoded) {
		return decodeURI(encoded);
	}

	$scope.loadDataModel = function() {

		var request = 
		{
			method: 'GET',
			url: suffixStaticUrlWithGuid($scope.model.url()),
		};

		function handleSuccess(response) { 

			$scope.model.bind(response);
			$scope.initWindowHash();
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

	$scope.gotoIframeView = function() {
		$scope.model.cancelSelection();

		$scope.view = Views.IFRAME; 
	};

	$scope.gotoContactView = function() {
		$scope.model.cancelSelection();

		window.location.hash = '#category=' + 'contact';
		$scope.view = Views.CONTACT; 
	};

	$scope.gotoAboutView = function() {
		$scope.model.cancelSelection();

		window.location.hash = '#category=' + 'about';
		$scope.view = Views.ABOUT; 
	};

	$scope.gotoPeopleView = function() {
		$scope.model.cancelSelection();

		window.location.hash = '#category=' + 'people';
		$scope.view = Views.PEOPLE; 
	};

	$scope.gotoHomeView = function() {
		$scope.model.cancelSelection();

		window.location.hash = '#category=' + 'home';
		$scope.view = Views.HOME; 
	};

	$scope.updateWindowHashForCurrentlySelectedCategory = function() {
		window.location.hash = '#category=' + $scope.model.selectedCategory + ';page=' + $scope.model.propertiesPageNumber;
	};

	$scope.setPropertiesPageNumber = function(number) {
		$scope.model.setPropertiesPageNumber(number);
		$scope.updateWindowHashForCurrentlySelectedCategory();
	};

	$scope.gotoCategoryView = function(category) {

		if (category === undefined)
			category = $scope.model.categories[0];

		$scope.model.cancelSelection();
		$scope.model.selectCategory(category);
		$scope.model.propertiesPageNumber = 1;

		$scope.updateWindowHashForCurrentlySelectedCategory();

		$scope.view = Views.CATEGORY; 
	};

	$scope.updateWindowHashForCurrentlySelectedProperty = function() {

		var property = $scope.model.selectedProperty;

		var category = (property.sold == false)
			? property.category
			: "sold";

		var propertyIndex = $scope.model.propertiesForCategory(category).indexOf(property);
		var windowHash = '#category=' + category + ';propertyIndex=' + propertyIndex.toString();
		window.location.hash = windowHash;
	};

	$scope.viewProperty = function(property) {
		$scope.view = Views.PROPERTY;
		$scope.model.selectProperty(property);
		$scope.updateWindowHashForCurrentlySelectedProperty();
	}

	$scope.gotoSoldView = function() {
		$scope.model.cancelSelection();
		$scope.view = Views.CATEGORY; 
		$scope.model.selectCategory('sold');
		$scope.model.setPropertiesPageNumber(1);
		$scope.updateWindowHashForCurrentlySelectedCategory();
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
			case Views.CONTACT:
				$scope.gotoContactView();
				break;
			case Views.ABOUT:
				$scope.gotoAboutView();
				break;
			case Views.PEOPLE:
				$scope.gotoPeopleView();
				break;
			}
	});

	$scope.respondToWindowHashChange = function(previousHash, currentHash) {

		if ((currentHash == null) || (currentHash.length <= 1)) {

			if ($scope.view !== Views.HOME) {
				$scope.view = Views.HOME;
			}

			return;
		}

		var pairStrings = currentHash.substring(1).split(';');

		var hash = {
			'category' : null,
			'propertyIndex' : null,
			'page' : null
		};

		pairStrings.forEach(function(pairString){
			var pair = pairString.split('=');
			hash[pair[0]] = pair[1];
		});

		hash['page'] = parseInt(hash['page']);
		if (isNaN(hash['page']) == true)
			hash['page'] = null;

		// specific property selected
		//
		if (hash['propertyIndex'] !== null) {

			var category = hash['category'];
			if ($scope.model.selectedCategory !== category) {
				$scope.model.selectCategory(category);
			}

			var propertyIndex = parseInt(hash['propertyIndex']);

			var property = $scope.model.propertiesForCategory(category)[propertyIndex];

			if (($scope.view !== Views.PROPERTY) || (property !== $scope.model.selectedProperty)) {
				
				if ($scope.view !== Views.PROPERTY)
					$scope.view = Views.PROPERTY;

				if (property !== $scope.model.selectedProperty)
					$scope.model.selectProperty( $scope.model.propertiesForCategory(category)[propertyIndex]);
			} 

			return;
		}
		// else is category
		//
		else if (hash['category'] !== null) {

			var category = hash['category'];

			if (category == 'home'){
				$scope.view = Views.HOME;
				return;
			}
			else if (category == 'contact') {
				$scope.view = Views.CONTACT;
				return;
			}
			else if (category == 'about') {
				$scope.view = Views.ABOUT;
				return;
			}
			else if (category == 'people') {
				$scope.view = Views.PEOPLE;
				return;
			}

			var page = hash['page'];

			if (
				($scope.view !== Views.CATEGORY) 
				|| 
				(category !== $scope.model.selectedCategory) 
				|| 
				($scope.model.propertiesPageNumber !== page)
				) {
				
				if ($scope.view !== Views.CATEGORY) {
					$scope.view = Views.CATEGORY;
				}

				if ($scope.model.selectedCategory !== category) {
					$scope.model.selectCategory(category);
				}
				
				if (page !== null) {
					if ($scope.model.propertiesPageNumber !== page)
						$scope.model.setPropertiesPageNumber(page);
				}
			} 

			return;
		}
	};

	$scope.windowHash = '';
	$scope.initWindowHash = function() {

		var hash = window.location.hash;

		if (hash.substring(0,2) === '##') {
		
			var url = hash.substring(2);
			window.location.hash = '';

			window.open(url, 'iframe');
			$scope.gotoIframeView();
		} 
		else {
			$scope.windowHash = hash;
			$scope.respondToWindowHashChange(null, hash);
		}

		// www.frprop.com/

		// 'http://localhost:8000/static/index.html##http://www.sapropertynews.co.za/residential-property/item/18164-things-to-consider-before-buying-an-investment-property'
	};	
	 
	$scope.windowHashWatcher = function() {

		var hash = window.location.hash;
		if (hash !== $scope.windowHash) {
			
			var oldHash = $scope.windowHash;
			$scope.windowHash = hash;

			$scope.respondToWindowHashChange(oldHash, hash);
		}
	};
	$scope.registerWindowHashWatcher = function() {
		$interval($scope.windowHashWatcher, 200);
	};

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

	$scope.mailToHref = function(toAddr, subject, cc) {

		var url = 'mailto:' + toAddr + '?Subject=' + encodeURIComponent(subject);
		
		if ((cc !== undefined) && (cc !== '') && (cc.length > 3))
			url = url + '&cc=' + encodeURIComponent(cc);

		console.log(url);

		return url;
	};

	$scope.enquireAfterPriceOfSelectedProperty = function() {

		var contact = $scope.model.contactsForCategory($scope.model.selectedProperty.category)[0];
		var cc = $scope.model.getCCContact();
		var subject = $scope.model.selectedProperty['name'];

		var href = $scope.mailToHref(contact['email'], subject, cc.email);
		window.open(href, '_blank');
	};

	$scope.emailPrimaryContact = function() {

		var contact = $scope.model.getPrimaryContact();
		var cc = $scope.model.getCCContact()

		var subject = 'Enquiry';

		var href = $scope.mailToHref(contact['email'], subject, cc.email);
		window.open(href, '_blank');
	};

	// -----------------------------------------------------------------
	/* SOCIAL LINKS */

	$scope.openUrlInNewWindow = function(url) {
		window.open(url, '_blank');
	}

	$scope.openFacebook = function() {
		$scope.openUrlInNewWindow('https://www.facebook.com/frprop');
	};

	$scope.openTwitter = function() {
		$scope.openUrlInNewWindow('https://twitter.com/FRprop');
	};

	$scope.openLinkedIn = function() {
		$scope.openUrlInNewWindow('http://www.linkedin.com/company/10080815?trk=tyah&trkInfo=clickedVertical%3Acompany%2CclickedEntityId%3A10080815%2Cidx%3A1-1-1%2CtarId%3A1442464963753%2Ctas%3Afisher%20roela');
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

	// ------------------------------------------------------

	$scope.selectNextPropertyInCategory = function() {
		$scope.model.selectNextPropertyInCategory();
		$scope.updateWindowHashForCurrentlySelectedProperty();
	};
	$scope.selectPreviousPropertyInCategory = function() {
		$scope.model.selectPreviousPropertyInCategory();
		$scope.updateWindowHashForCurrentlySelectedProperty();
	};

	// -----------------------------------------------------------------
	// INIT

	$scope.loadDataModel();
	$timeout($scope.init_twitter_widget, 500);
	$scope.registerWindowHashWatcher();
};