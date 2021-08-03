var settings = require('../settings.json');
var path=require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
settings.webpack.output.path=settings.webpack.output.path.replace("./",path.resolve(__dirname)+"/")
console.log("#########",settings.webpack.output.path)
module.exports = {
    entry: settings.webpack.entry,
    output: settings.webpack.output,
    /*
    output: {
     filename: '[name].bundle.js',
     path: path.resolve(__dirname, 'dist'),
     clean: true,
    },
    */
    plugins: [

    ],
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

 };