var TrackColours = Object.freeze([

	Colour.BLACK, 
	Colour.BLUE, 
	Colour.PURPLE, 
	Colour.DARKGREEN, 
	Colour.RED
]);

function TracksController($rootScope, $scope, $http, $timeout) {

	$scope.getUnusedTrackColour = function() {

		var inUse = $scope.$parent.tracks
			.map(function(x) { return x.colour; });

		var unUsed = TrackColours
			.filter(function(x) { return inUse.indexOf(x) == -1; });

		return (unUsed.length > 0) ? unUsed[0] : [Colour.BLACK];
	};

	// LOAD

	$scope.loadTrack = function(id) {

		var matches = $scope.$parent.tracks
			.filter(function(track){return (track.id == id);});
		
		if (matches.length > 0)
			return;

		var successFn = function(data) { 

			var newTrack = new Track(data.track);
			newTrack.colour = $scope.getUnusedTrackColour();
			$scope.$parent.tracks.push(newTrack);

			$rootScope.$emit(Event.TRACK_LOADED, newTrack.id);
		};

		var failFn = function(status){
			console.log('fail');
		};

		httpGET($http, 'track', { 'id' : id }, successFn, failFn, $scope.globalDebug);
	};
	
 	$rootScope.$on(Command.LOAD_TRACK, function(evt, id) {
		$scope.loadTrack(id);	
	});

 	// UNLOAD

	$scope.unloadTrack = function (id) {

		$scope.$parent.tracks.removeWhere(function(track) { return (track.id == id); });
		$rootScope.$emit(Event.TRACK_UNLOADED);
	};

	$scope.reloadTrack = function (id) {

		$scope.$parent.tracks.removeWhere(function(track) { return (track.id == id); });
		$rootScope.$emit(Event.TRACK_UNLOADED);
		$rootScope.$emit(Command.LOAD_TRACK, id);
	};

	// EXPORT

	$scope.exportTrack = function(id) {
		
		var fileName = $scope.$parent.tracks
			.first(function(track) { return (track.id == id); })
			.name + '.gpx'
		
		$rootScope.$emit(Command.EXPORT_TRACKS, { ids : [id], fileName : fileName});
	};

	$scope.exportAllTracks = function() {

		var ids = $scope.$parent.tracks.map(function(track) { return track.id; });		
		$rootScope.$emit(Command.EXPORT_TRACKS, { ids : ids });
	};

	$scope.saveTrack = function(id) {

	};
};