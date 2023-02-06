const path = require('path')
const merge = require('webpack-merge')
const base = require('./base.config')("production")

const resolve = (filePath) => path.resolve(__dirname, filePath)

module.exports = merge(base, {
    mode: 'production',
    devtool: 'source-map',
    output: {
        path: resolve('../../backend/static'),
        publicPath: '/static/',
        filename: 'js/[name].[contenthash].js',
        chunkFilename: 'js/[name].[contenthash].js',
    },
})
