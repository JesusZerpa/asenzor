const path=require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
let name=__dirname.split("/").splice(-1)

module.exports = {
    entry: __dirname+"/"+name+".py",
    output: path.resolve(__dirname+"/../../dist/main.js"),
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
        modules: [
            path.resolve(__dirname, '../node_modules'), 
            'node_modules'],
        alias: {
            
            "Root":path.resolve( __dirname,"apps"),
            "System":path.resolve( __dirname),
            'vue': 'vue/dist/vue.esm.js',

        }
    },

 };