const path = require('path')
const merge = require('webpack-merge')
const base = require('./base.config')("dev")

const resolve = (filePath) => path.resolve(__dirname, filePath)

module.exports = merge(base, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        contentBase: resolve('../dist'),
        hot: true,
        port: 8080,
        disableHostCheck: true,
        historyApiFallback: true,
        proxy: {
            '/api': 'http://localhost:9979',
            '/webapi': 'http://localhost:9979',
            changeOrigin: true
        }
    },
    output: {
        filename: '[name].bundle.js',
        path: resolve('../dist'),
        publicPath: '/',
    },
})
