'use strict';

describe('Component: ExperimentalProtocolComponent', function() {
  // load the controller's module
  beforeEach(module('mozaikRepositoryApp.experimental-protocol'));

  var ExperimentalProtocolComponent;

  // Initialize the controller and a mock scope
  beforeEach(inject(function($componentController) {
    ExperimentalProtocolComponent = $componentController('experimental-protocol', {});
  }));

  it('should ...', function() {
    expect(1).toEqual(1);
  });
});
