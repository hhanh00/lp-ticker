In this article, we are going to build a web application that shows
the prices of a Uniswap trading pair on the Ethereum blockchain.

At the end, the application will look as follows.

Let's start with a tree structure:
```
.
├── README.md
├── ticker-be
├── ticker-fe
└── ticker-svc
```

# FE

```
yarn init
yarn add nuxt @nuxtjs/axios bootstrap bootstrap-vue luxon lightweight-charts
yarn add -D pug pug-plain-loader
```

```js
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
}
```

Create `pages/index.vue`

```html
<template lang='pug'>
  .container
    h1.title BTC/ETH
    form
      label(for='start_date') Start Date
      b-form-datepicker#start_date(v-model='start_date')
      label(for='end_date') End Date
      b-form-datepicker#end_date(v-model='end_date')
      b-button.mt-2(variant='primary' @click='update_chart') Update Chart
</template>

<script>
import {DateTime} from 'luxon'

export default {
  data() {
    return {
      start_date: DateTime.local().plus({week: -1}).toISODate(),
      end_date: DateTime.local().toISODate(),
    }
  },
  methods: {
    update_chart() {
    }
  }
}
</script>
```

Change `index.vue` to

```
  <template lang='pug'>
  ...
    form
      label(for='start_date') Start Date
      b-form-datepicker#start_date(v-model='start_date')
      label(for='end_date') End Date
      b-form-datepicker#end_date(v-model='end_date')
      b-button.mt-2(variant='primary' @click='update_chart') Update Chart
    #chart.mt-4(ref='chart')
  </template>

  <script>
  ...

  export default {
    mounted() {
      const chart = LightweightCharts.createChart(this.$refs.chart, { 
        height: 300,
        timeScale: {
          timeVisible: true,
          secondsVisible: true
        }
      })
      const lineSeries = chart.addLineSeries()
      this.lineSeries = lineSeries
      this.update_chart()
    },
    ...
    methods: {
      async update_chart() {
        const r0 = await this.$axios({
          method: 'GET',
          url: '/api/data',
          params: {
            start_date: this.start_date,
            end_date: this.end_date
          }
        })
        const data = r0.data
        this.lineSeries.setData(data)
      }
    }
  }
```

Put some mock data in `static/api/data`

```json
[
    {
        "time": "2019-04-11",
        "value": 180.01
    },
    {
        "time": "2019-04-12",
        "value": 96.63
    },
    {
        "time": "2019-04-13",
        "value": 76.64
    },
    {
        "time": "2019-04-14",
        "value": 81.89
    },
    {
        "time": "2019-04-15",
        "value": 74.43
    },
    {
        "time": "2019-04-16",
        "value": 80.01
    },
    {
        "time": "2019-04-17",
        "value": 96.63
    },
    {
        "time": "2019-04-18",
        "value": 76.64
    },
    {
        "time": "2019-04-19",
        "value": 81.89
    },
    {
        "time": "2019-04-20",
        "value": 74.43
    }
]
```

Generate static website

`yarn run nuxt generate`

