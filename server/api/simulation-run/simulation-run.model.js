'use strict';

import mongoose from 'mongoose';

var ResultSchema = new mongoose.Schema({
	class_name: String,
	file_name: String,
	figure: {type: mongoose.Schema.Types.Object, ref: 'GFS' },
	parameters: Object
});

var SimulationRunSchema = new mongoose.Schema({
  submission_date: String,
  run_date: String,
  parameters: Object,
  results: [ResultSchema],
  simulation_run_name: String,
  model_name: String
});

var ParameterSearchSchema = new mongoose.Schema({
  submission_date: String,
  name: String,
  simulation_runs: [SimulationRunSchema],
  parameter_combinations: Object
});


export var GFS = mongoose.model("GFS", new mongoose.Schema({}, {strict: false}), "fs.files" );
export var ParameterSearch = mongoose.model('parameterSearchRun', ParameterSearchSchema,'parameterSearchRuns');
export default mongoose.model('submission', SimulationRunSchema);
