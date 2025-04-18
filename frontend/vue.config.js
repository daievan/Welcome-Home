module.exports = {
  publicPath: '/', // Flask 会通过模板渲染 index.html，不需要 /static/ 前缀
  assetsDir: 'static', // 所有 JS/CSS 图片都输出到 dist/static/
  transpileDependencies: []
}
