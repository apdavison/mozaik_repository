'use strict';

export function routeConfig($routeProvider, $locationProvider) {
  'ngInject';
  $routeProvider
    .otherwise({
      redirectTo: '/simruns/'
    });


  $locationProvider.html5Mode(true);
}
