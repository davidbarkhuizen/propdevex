var StaticSiteControllers = angular.module('StaticSiteControllers', []);

var commonDependencies = [ '$rootScope', '$scope', '$http', '$timeout', '$interval']; 

var controllers = [
	['GodController', [GodController]],
];

controllers.forEach(function(ctrl) { 
	StaticSiteControllers.controller(ctrl[0], commonDependencies.concat(ctrl[1]));
});

var appName = 'StaticSite';
var appControllers = ['StaticSiteControllers'];  
var StaticSite = angular.module(appName, appControllers);