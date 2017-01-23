'use strict';
/*eslint no-process-env:0*/

// Development specific configuration
// ==================================
module.exports = {

  // MongoDB connection options
  mongo: {
    uri: process.env.MONGODB_URI
     // || 'mongodb://localhost/mozaikrepository'
  }
  },

  // Seed database on startup
  seedDB: false

};
