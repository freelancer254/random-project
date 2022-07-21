import { createApp } from 'vue'
import App from './App.vue'

//from PrimeVue
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import TabMenu from 'primevue/tabmenu'
import Fieldset from 'primevue/fieldset'
import InputText from 'primevue/inputtext'
//for datatable
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ColumnGroup from 'primevue/columngroup'     //optional for column grouping
import Row from 'primevue/row'                     //optional for row

//primevue styling
import 'primevue/resources/themes/saga-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

//create App
const app = createApp(App);

app.use(PrimeVue);
app.component('Button', Button)
app.component('TabMenu', TabMenu)
app.component('Fieldset', Fieldset)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)
app.component('Row', Row)
app.component('InputText', InputText)


app.mount('#app')
