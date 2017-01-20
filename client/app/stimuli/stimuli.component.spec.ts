'use strict';

describe('Component: StimuliComponent', function() {
  // load the controller's module
  beforeEach(module('mozaikRepositoryApp.stimuli'));

  var StimuliComponent;

  // Initialize the controller and a mock scope
  beforeEach(inject(function($componentController) {
    StimuliComponent = $componentController('stimuli', {});
  }));

  it('should ...', function() {
    expect(1).toEqual(1);
  });
});
