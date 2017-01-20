'use strict';

describe('Component: ParamViewComponent', function() {
  // load the controller's module
  beforeEach(module('mozaikRepositoryApp.param-view'));

  var ParamViewComponent;

  // Initialize the controller and a mock scope
  beforeEach(inject(function($componentController) {
    ParamViewComponent = $componentController('param-view', {});
  }));

  it('should ...', function() {
    expect(1).toEqual(1);
  });
});
