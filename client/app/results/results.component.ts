'use strict';
const angular = require('angular');
const ngRoute = require('angular-route');
const bootstrapLightbox = require('angular-bootstrap-lightbox');

require('angular-bootstrap-lightbox/dist/angular-bootstrap-lightbox.css');

import './results.css';


import routes from './results.routes';

export class ResultsComponent {
  $http; 
  simRun;
  resId;
  images=[];

  /*@ngInject*/
  constructor($http,$route,Lightbox) {
    this.$http = $http;
    this.resId = $route.current.params.simRunId
    this.lightbox = Lightbox
  }

  openLightboxModal(index) {
    this.lightbox.openModal(this.images, index);
  };


  $onInit() {
    this.$http.get('/api/simulation-runs/result/'+this.resId).then(response => {
      this.simRun = response.data;
      for (let res of this.simRun.results)
      {
        this.images.push({
          'url': '/api/simulation-runs/images/'+res.figure._id,
          //'caption': res.file_name,
          //'thumbUrl': 'thumb1.jpg' // used only for this example
        })
      } 

    });
  }
}

export default angular.module('mozaikRepositoryApp.results', [ngRoute,'bootstrapLightbox'])
  .config(routes)
  .component('results', {
    template: require('./results.html'),
    controller: ResultsComponent,
    //controllerAs: 'resultsCtrl'
  })
  .name;
