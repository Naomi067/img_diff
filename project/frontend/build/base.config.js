const path = require('path')
const {VueLoaderPlugin} = require('vue-loader')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const {CleanWebpackPlugin} = require('clean-webpack-plugin')
const WebpackBar = require('webpackbar')

const resolve = (filePath) => path.resolve(__dirname, filePath)

module.exports = (buildMode) => {
    const CssHandleLoader = [
        {
            loader: MiniCssExtractPlugin.loader,
            options: {
                publicPath: buildMode === 'dev'? '/': "/static",
            },
        },
        {
            loader: 'css-loader',
        },
        {
            loader: 'postcss-loader',
            options: {
                postcssOptions: {
                    plugins: [['postcss-preset-env', {}]],
                },
            },
        },
    ]
    return {
        entry: resolve('../src/main.js'),
        resolve: {
            extensions: ['.js', '.vue', '.json', '.css'],
            alias: {
                '@': resolve('../src'),
                vue$: 'vue/dist/vue.esm.js',
            },
        },
        module: {
            rules: [
                {
                    test: /\.css$/,
                    use: [
                        ...CssHandleLoader,
                    ],
                },
                {
                    test: /\.less$/,
                    use: [
                        ...CssHandleLoader,
                        'less-loader',
                    ],
                },
                {
                    test: /\.scss$/,
                    use: [
                        'vue-style-loader',
                        'css-loader',
                        'sass-loader'
                    ]
                },
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader',
                        },
                    ],
                },
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    // 优先执行
                    enforce: 'pre',
                    loader: 'eslint-loader',
                    options: {
                        fix: true,
                    },
                },
                {
                    test: /\.vue$/,
                    use: [
                        {
                            loader: 'vue-loader',
                        },
                    ],
                },
                {
                    // webpack5 内置了 asset 模块, 用来代替 file-loader & url-loader & raw-loader 处理静态资源
                    test: /\.png|jpg|gif|jpeg|svg/,
                    type: 'asset',
                    parser: {
                        dataUrlCondition: {
                            maxSize: 10 * 1024,
                        },
                    },
                    generator: {
                        filename: 'images/[name]_[contenthash][ext]',
                    },
                },
                {
                    // 解析字体
                    test: /\.(woff|woff2|eot|ttf|otf)$/,
                    type: 'asset',
                    parser: {
                        dataUrlCondition: {
                            maxSize: 10 * 1024,
                        },
                    },
                    generator: {
                        filename: 'fonts/[base]',
                    },
                },
            ],
        },
        plugins: [
            new MiniCssExtractPlugin(
              {
                  filename: 'css/[name].[hash:10].css',
              },
            ),
            new WebpackBar(),
            new VueLoaderPlugin(),
            new CleanWebpackPlugin(),
            new HtmlWebpackPlugin({
                title: 'L32时装对比',
                template: resolve('../public/index.html'),
                favicon: resolve('../public/favicon.ico'),
            }),
        ],
    }
}
