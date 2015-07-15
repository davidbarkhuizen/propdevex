var PropDevExControllers = angular.module('PropDevExControllers', []);

var commonDependencies = [ '$rootScope', '$scope', '$http', '$timeout']; 

var controllers = [
	['GodController', [GodController]],
	['ModalController', [ModalController]],
	['SocialController', [SocialController]],
];

controllers.forEach(function(ctrl) { 
	PropDevExControllers.controller(ctrl[0], commonDependencies.concat(ctrl[1]));
});

var appName = 'PropDevEx';
var appControllers = ['PropDevExControllers'];  
var PropDevEx = angular.module(appName, appControllers);