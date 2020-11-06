In this article, we are going to build a web application that shows
the prices of a Uniswap trading pair on the Ethereum blockchain.

At the end, the application will look as follows.

Let's start with a tree structure:
```
.
├── README.md
├── ticker_be
├── ticker_fe
└── ticker_svc
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

# BE

In `ticker`, create python venv

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install django djangorestframework
$ django-admin startproject ticker_be
```

In `ticker_be`
```
./manage.py startapp api
```

In `ticker_be/settings.py`, add `api` in `INSTALLED_APPS`,
Then migrate the database
```
$ ./manage.py migrate
```

Create a `urls.py` in `api`,

```python
from django.urls import path
from . import views

urlpatterns = [
  path('data', views.get_data)
]
```

In `views.py`, start with

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_data(request):
  return Response()
```

In `urls.py` of the main folder
```
from django.urls import path, include # <-- ADD THIS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')), # <--- ADD THIS
]
```

`curl http://localhost:8000/api/data`

In `models.py`
```python
class PriceItem(models.Model):
  time = models.DateTimeField(unique=True)
  value = models.DecimalField(max_digits=12, decimal_places=4)
```

Add a `serializers.py` file
```python
from rest_framework import serializers
from .models import PriceItem

class TimestampField(serializers.Field):
  def to_representation(self, value):
    return value.timestamp()

class PriceItemSerializer(serializers.ModelSerializer):
  time = TimestampField()
  class Meta:
    model = PriceItem
    fields = ['time', 'value']
```

Change `views.py`
```python
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import status
from .models import PriceItem
from .serializers import PriceItemSerializer

@api_view(['GET', 'POST'])
def get_data(request):
  if request.method == 'POST':
    data = request.data
    try:
      PriceItem.objects.create(time=data['time'], value=data['value'])
    except IntegrityError:
      pass
    return Response(status=status.HTTP_201_CREATED)
  else:
    start_date = timezone.make_aware(datetime.strptime(request.GET['start_date'], '%Y-%m-%d'))
    end_date = timezone.make_aware(datetime.strptime(request.GET['end_date'], '%Y-%m-%d')) + timedelta(days=1)
    items = PriceItem.objects.filter(time__gte=start_date, time__lte=end_date)
    ser = PriceItemSerializer(items, many=True)
    return Response(ser.data)
```

Make migrations
```
./manage.py makemigrations
./manage.py migrate
```

`curl 'http://localhost:8000/api/data?start_date=2020-11-04&end_date=2020-12-01'`

```sh
curl --location --request POST 'http://localhost:8000/api/data' \
--header 'Content-Type: application/json' \
--data-raw '{"time": "2020-11-04","value": 100}'
```
