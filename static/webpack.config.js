var settings = require('../settings.json');
var path=require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
console.log(settings)


module.exports = {
    devtool: 'inline-source-map',
    context: __dirname,
    entry: settings.webpack.entry,
    mode:"production",//"development","production"
    output: settings.webpack.output,
   module:{
   	rules: [
            {
                test: /\.py$/,
                loader: 'transcrypt-loader',
            
               
            }
        ],
   },
    resolve: {

        alias: {
            
            "Root":path.resolve( __dirname,"apps"),
            "System":path.resolve( __dirname),
            'vue': 'vue/dist/vue.esm.js',

        }
    },



}