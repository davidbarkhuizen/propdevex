var PropDevExControllers = angular.module('PropDevExControllers', []);

var commonDependencies = [ '$rootScope', '$scope', '$http', '$timeout', '$interval']; 

var controllers = [
	['GodController', [GodController]],
	['ModalController', [ModalController]],
];

controllers.forEach(function(ctrl) { 
	PropDevExControllers.controller(ctrl[0], commonDependencies.concat(ctrl[1]));
});

var appName = 'PropDevEx';
var appControllers = ['PropDevExControllers'];  
var PropDevEx = angular.module(appName, appControllers);