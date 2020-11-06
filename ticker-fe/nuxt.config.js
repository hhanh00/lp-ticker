export default {
  target: 'static',

  head: {
    title: 'lp-ticker',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    script: [
      { src: 'https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js' }
    ]
  },

  modules: [
    'bootstrap-vue/nuxt',
    '@nuxtjs/axios',
  ],

  axios: {
    proxy: true
  },

  proxy: {
    '/api': 'http://localhost:8000/',
  }
}
