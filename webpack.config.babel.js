import path from 'path';
import zlib from 'zlib';
import AssetsManifestPlugin from 'webpack-assets-manifest';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import { CleanWebpackPlugin } from 'clean-webpack-plugin';
import CompressionPlugin from 'compression-webpack-plugin';

import postCSSAutoPrefixer from 'autoprefixer';
import postCSSNesting from 'postcss-nesting';
import postCSSMixins from 'postcss-mixins';
import postCSSNano from 'cssnano';

const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

const ENV = process.env.NODE_ENV || 'development';
const isDev = ENV !== 'production';

const outputPath = path.resolve(__dirname, 'ponyfiction');
const outputName = `[name].${isDev ? 'dev' : '[contenthash]'}`;

const postCSSOptions = {
  plugins: [
    postCSSAutoPrefixer(),
    postCSSMixins(),
    postCSSNesting(),
    postCSSNano({
      preset: ['default', {
        discardComments: !isDev,
        normalizeWhitespace: !isDev,
      }],
    }),
  ],
};

const cssLoaderOptions = {
  modules: false,
  importLoaders: 1,
  url: true,
};

const extractLoaderOptions = {
  publicPath: './',
};

const defaultPlugins = [
  new MiniCssExtractPlugin({
    filename: `${outputName}.css`,
    chunkFilename: '[id].css',
  }),
  new CleanWebpackPlugin(),
  new AssetsManifestPlugin({
    output: 'manifest.json',
    integrity: true,
    integrityHashes: ['sha256'],
    customize: (_, original) => original,
  }),
];

const devPlugins = [
  new BundleAnalyzerPlugin({ analyzerMode: 'static', openAnalyzer: false }),
];

const productionPlugins = [
  new CompressionPlugin({
    filename: '[path][base].gz',
    algorithm: 'gzip',
    exclude: /.map$/,
  }),
  new CompressionPlugin({
    filename: '[path][base].br',
    algorithm: 'brotliCompress',
    exclude: /.map$/,
    compressionOptions: {
      params: {
        [zlib.constants.BROTLI_PARAM_QUALITY]: 19,
      },
    },
  }),
];

module.exports = {
  mode: ENV,
  context: path.resolve(__dirname, 'src'),
  entry: {
    index: './index.css',
  },

  output: {
    path: outputPath,
    publicPath: '/localstatic/ponyfiction/',
    filename: `${outputName}.js`,
  },

  resolve: {
    extensions: ['.jsx', '.js', '.json', 'png', '.jpg', '.gif', '.svg', '.eot', '.ttf', '.woff', '.woff2'],
    modules: [
      path.resolve(__dirname, 'src'),
      path.resolve(__dirname, 'node_modules'),
      'node_modules',
    ],
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          { loader: MiniCssExtractPlugin.loader, options: extractLoaderOptions },
          { loader: 'css-loader', options: cssLoaderOptions },
          { loader: 'postcss-loader', options: { postcssOptions: postCSSOptions } },
        ],
      },
      {
        test: /\.(png|jpg|gif|eot|ttf|woff|woff2)$/,
        type: 'asset',
        parser: {
          dataUrlCondition: {
            maxSize: 8192,
          },
        },
      },
    ],
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
          index: {
          name: 'index',
          type: 'css/mini-extract',
          chunks: 'all',
          enforce: true,
        },
      },
    },
  },
  plugins: [...defaultPlugins, ...(isDev ? devPlugins : productionPlugins)],

  stats: { colors: true },

  node: {
    global: true,
    __filename: false,
    __dirname: false,
  },

  devtool: 'source-map',
};
