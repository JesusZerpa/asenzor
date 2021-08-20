 const merge = require('webpack-merge');
 const common = require('./webpack.common.js');

 module.exports = merge(common, {
   mode: 'development',
   watch:false,
   devtool: 'inline-source-map',
   devServer: {
     contentBase: './dist',
   },
 });