"""
This tool adds simulation run to the mozaik repository, or a collection of mozaik simulation runs
that were a result of a parameter search.

usage:

if adding single run:

python add_mozaik_repository.py path_to_mozaik_simulation_run_output_directory

if adding parameter search:

python add_mozaik_repository.py path_to_mozaik_parameter_search_output_directory name_of_the_simulation
"""
import numpy
from pymongo import MongoClient
import gridfs
from sphinx.util.docstrings import prepare_docstring
from mozaik.tools.distribution_parametrization import MozaikExtendedParameterSet, load_parameters,PyNNDistribution
from mozaik.storage.datastore import *
from parameters import ParameterSet
from mozaik.tools.mozaik_parametrized import MozaikParametrized
from mozaik.tools.misc import result_directory_name
import re
from sphinx.util import docstrings
import sys
import os.path
from parameters.random import ParameterDist
import datetime
import json
import pickle
import imageio

PARAM_OR_RETURNS_REGEX = re.compile(":(?:param|returns)")
RETURNS_REGEX = re.compile(":returns: (?P<doc>.*)", re.S)
PARAM_REGEX = re.compile(":param (?P<name>[\*\w]+): (?P<doc>.*?)"
                         "(?:(?=:param)|(?=:return)|(?=:raises)|\Z)", re.S)


def reindent(string):
    return "\n".join(l.strip() for l in string.strip().split("\n"))

def parse_docstring(docstring):
    """Parse the docstring into its components.
    :returns: a dictionary of form
              {
                  "short_description": ...,
                  "long_description": ...,
                  "params": [{"name": ..., "doc": ...}, ...],
                  "returns": ...
              }
    """

    short_description = long_description = returns = ""
    params = []

    if docstring:
        docstring = "\n".join(docstrings.prepare_docstring(docstring))

        lines = docstring.split("\n", 1)
        short_description = lines[0]

        if len(lines) > 1:
            long_description = lines[1].strip()

            params_returns_desc = None

            match = PARAM_OR_RETURNS_REGEX.search(long_description)
            if match:
                long_desc_end = match.start()
                params_returns_desc = long_description[long_desc_end:].strip()
                long_description = long_description[:long_desc_end].rstrip()

            if params_returns_desc:
                params = [
                    {"name": name, "doc": doc}
                    for name, doc in PARAM_REGEX.findall(params_returns_desc)
                ]

                match = RETURNS_REGEX.search(params_returns_desc)
                if match:
                    returns = reindent(match.group("doc"))

    return {
        "short_description": short_description,
        "long_description": long_description,
        "params": params,
        "returns": returns
    }


class ParametersEncoder(json.JSONEncoder):
    """
    For encoding parameters
    """
    def default(self, obj):
            if isinstance(obj, ParameterDist) or isinstance(obj, PyNNDistribution):
                return str(obj)
            
            return json.JSONEncoder.default(self, obj)

def openMongoDB():
    #### MONGODB STUFF #######
    client = MongoClient()
    db = client["mozaikrepository"]
    gfs = gridfs.GridFS(db)
    return gfs,db


def createSimulationRunDocumentAndUploadImages(path,gfs):

    data_store = PickledDataStore(load=True,parameters=ParameterSet({'root_directory':path,'store_stimuli' : False}),replace=False)
    
    #lets get parameters
    param = load_parameters(os.path.join(path,'parameters'),{})


    ##### STIMULI ###########
    stimuli = [MozaikParametrized.idd(s) for s in data_store.get_stimuli()]
    unique_stimuli = [MozaikParametrized.idd(s) for s in set(data_store.get_stimuli())]
    stimuli_types = {}
    for s in stimuli: stimuli_types[s.name]=True

    stim_docs = []
    for s in unique_stimuli:
        print str(s)
        print data_store.sensory_stimulus.keys()
        raws = data_store.get_sensory_stimulus([str(s)])[0]
        if raws == None:
            raws= numpy.array([[[0,0],[0,0.1]],[[0,0],[0,0]]])
        
        imageio.mimwrite('movie.gif', raws,duration=param['input_space']['update_interval']/1000.0)
        stim_docs.append({
         'class' : s.name,
         'params' : s.get_param_values(),
         'short_description' : parse_docstring(getattr(__import__(s.module_path, globals(), locals(), s.name),s.name).__doc__)["short_description"],
         'long_description' : parse_docstring(getattr(__import__(s.module_path, globals(), locals(), s.name),s.name).__doc__)["long_description"],
         'gif'    : gfs.put(open('movie.gif','r')),
        })
    
    ##### RECORDERS ###################
    recorders_docs = []
    for sh in param["sheets"].keys():
        for re in param['sheets'][sh]["params"]["recorders"].keys():
            recorder = param['sheets'][sh]["params"]["recorders"][re]
            name = recorder["component"].split('.')[-1]
            module_path = '.'.join(recorder["component"].split('.')[:-1])
            recorders_docs.append({
             'class' : name,
             'source' : sh,
             'params' : recorder["params"],
             'variables' : recorder["variables"],
             'short_description' : parse_docstring(getattr(__import__(module_path, globals(), locals(), name),name).__doc__)["short_description"],
             'long_description' : parse_docstring(getattr(__import__(module_path, globals(), locals(), name),name).__doc__)["long_description"],
            })
            

    # load basic info
    f = open(os.path.join(path,'info'),'r')
    info = eval(f.read())        

    
    #let load up results
    results = []
    f = open(os.path.join(path,'results'),'r')
    for line in f:
        r = eval(line)
        r["figure"] =   gfs.put(open(os.path.join(path,r['file_name']),'r'))
        results.append(r)

    document = {
        'submission_date' :     datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S'),
        'run_date'        :     info["creation_data"],
        'simulation_run_name' : info["simulation_run_name"],
        'model_name' : info["model_name"],
        'results' : results,
        'stimuli' : stim_docs,
        'recorders' : recorders_docs,
        'parameters' : json.dumps(param,cls=ParametersEncoder)
    }
    return document

assert len(sys.argv)>1 , "Not enough arguments, missing mozaik repository directory. Usage:\npython add_mozaik_repository.py path_to_mozaik_simulation_run_output_directory\n\nor\n\npython add_mozaik_repository.py path_to_mozaik_parameter_search_output_directory name_of_the_simulation"

gfs,db = openMongoDB()

if os.path.exists(os.path.join(sys.argv[1],'parameter_combinations')):

    assert len(sys.argv)>2, """Missing simulation run argument. Usage: \n python add_mozaik_repository.py path_to_mozaik_parameter_search_output_directory name_of_the_simulation """

    master_results_dir = sys.argv[1]

    f = open(master_results_dir+'/parameter_combinations','rb')
    combinations = pickle.load(f)
    f.close()
        
    # first check whether all parameter combinations contain the same parameter names
    assert len(set([tuple(set(comb.keys())) for comb in combinations])) == 1 , "The parameter search didn't occur over a fixed set of parameters"

    print combinations[0]

    simulation_runs = []
    for i,combination in enumerate(combinations):
        rdn = result_directory_name('ParameterSearch',sys.argv[2],combination)
        print rdn
        simulation_runs.append(createSimulationRunDocumentAndUploadImages(os.path.join(master_results_dir,rdn),gfs))


    document = {
            'submission_date' :     datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S'),
            'name' : master_results_dir,
            'simulation_runs' : simulation_runs,
            'parameter_combinations' : json.dumps(combinations)
    }

    db.parameterSearchRuns.insert_one(document)
else:
    db.submissions.insert_one(createSimulationRunDocumentAndUploadImages(sys.argv[1],gfs))

