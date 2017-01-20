'use strict';
const angular = require('angular');
const ngRoute = require('angular-route');
const uiBootstrap = require('angular-ui-bootstrap')

import routes from './experimental-protocol.routes';

export class ExperimentalProtocolComponent {  
  $http;
  $uibModal;
  simRun;
  simRunId;
  
  /*@ngInject*/
  constructor($http,$route,$uibModal) {
    this.$http = $http;
    this.simRunId = $route.current.params.simRunId;
    this.$uibModal = $uibModal;
  }

  paramsModal(params) {
    this.$uibModal.open({
      animation: true,
      ariaLabelledBy: 'modal-title-bottom',
      ariaDescribedBy: 'modal-body-bottom',
      template: '<div ng-repeat="(key,value) in $ctrl.params" style="margin:10px"><span style="width:300px;float : left;">{{key}}</span> <span>{{value}}</span></div>',
      controllerAs : '$ctrl',
      controller: function() {
        this.params = params;  
      }
    });
  }

  $onInit() {
    this.$http.get('/api/simulation-runs/result/'+this.simRunId).then(response => {
      this.simRun = response.data;
    });
  }
}

export default angular.module('mozaikRepositoryApp.experimental-protocol', [ngRoute,'ui.bootstrap'])
  .config(routes)
  .component('experimentalProtocol', {
    template: require('./experimental-protocol.html'),
    controller: ExperimentalProtocolComponent,
    //controllerAs: 'experimentalProtocolCtrl'
  })
  .name;
