function SocialController($rootScope, $scope, $http, $timeout) {

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

	// $timeout($scope.init_twitter_widget, 500);
};