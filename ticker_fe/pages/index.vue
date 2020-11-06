<template lang='pug'>
  .container
    h1.title BTC/ETH
    form
      label(for='start_date') Start Date
      b-form-datepicker#start_date(v-model='start_date')
      label(for='end_date') End Date
      b-form-datepicker#end_date(v-model='end_date')
      b-button.mt-2(variant='primary' @click='update_chart') Update Chart
    #chart.mt-4(ref='chart')
</template>

<script>
import {DateTime} from 'luxon'

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
  data() {
    return {
      start_date: DateTime.local().plus({week: -1}).toISODate(),
      end_date: DateTime.local().toISODate(),
    }
  },
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
</script>

