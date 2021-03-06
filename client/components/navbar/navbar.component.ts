'use strict';
/* eslint no-sync: 0 */
const angular = require('angular');

export class NavbarComponent {
  menu = [{
    'title': 'Simulation runs',
    'link': '/'
  },
  {
    'title': 'Parameter searches',
    'link': '/parameter-search'
  }
  ];
  $location;
  isLoggedIn: Function;
  isAdmin: Function;
  getCurrentUser: Function;
  isCollapsed = true;

  constructor($location, Auth) {
    'ngInject';
    this.$location = $location;
    this.isLoggedIn = Auth.isLoggedInSync;
    this.isAdmin = Auth.isAdminSync;
    this.getCurrentUser = Auth.getCurrentUserSync;
  }

  isActive(route) {
    return route === this.$location.path();
  }
}

export default angular.module('directives.navbar', [])
  .component('navbar', {
    template: require('./navbar.html'),
    controller: NavbarComponent
  })
  .name;
