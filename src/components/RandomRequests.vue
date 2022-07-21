<template>
  <div>
    <DataTable :value="draws" :paginator="true" class="p-datatable-draws" :rows="10"
            dataKey="key" :rowHover="true" v-model:selection="selectedDraws" v-model:filters="filters" filterDisplay="menu" :loading="loading"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
            :globalFilterFields="['key','username','timestamp','description']" responsiveLayout="scroll">
            <template #header>
                 <div class="flex justify-content-center align-items-center">
                    <center><h5 class="m-0">Random Requests</h5>
                              <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global'].value" placeholder="Search..." />
                    </span>
                    </center>
                   
                 </div>
            </template>
            <template #empty>
                No draws found.
            </template>
            <template #loading>
                Loading draws data. Please wait.
            </template>
            <Column selectionMode="single" headerStyle="width: 3rem"></Column>
            <Column field="key" header="Draw ID" sortable style="min-width: 14rem">
                <template #body="{data}">
                    {{data.key}}
                </template>
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter" placeholder="Search by ID"/>
                </template>
            </Column>
            <Column field="username" header="Username" sortable style="min-width: 14rem">
                <template #body="{data}">
                    {{data.username}}
                </template>
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter" placeholder="Search by Username"/>
                </template>
            </Column>
          
            <Column field="timestamp" header="Timestamp" sortable dataType="date" style="min-width: 8rem">
                <template #body="{data}">
                    {{data.timestamp}}
                </template>
                <template #filter="{filterModel}">
                    <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" />
                </template>
            </Column>
            <Column field="description" header="Description" sortable style="min-width: 14rem">
                <template #body="{data}">
                    {{data.description}}
                </template>
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter" placeholder="Search by Description"/>
                </template>
            </Column>
            <Column field="items" header="Items" sortable style="min-width: 14rem">
                <template #body="{data}">
                    {{data.items}}
                </template>
                
            </Column>
            <Column field="selected" header="Selected" sortable style="min-width: 14rem">
                <template #body="{data}">
                    {{data.selected}}
                </template>
                
            </Column>
        </DataTable>
  </div>

</template>

<script>
import {FilterMatchMode,FilterOperator} from 'primevue/api';

export default {
        data() {
        return {
            draws:null,
            selectedDraws: null,
            filters: {
                'global': {value: null, matchMode: FilterMatchMode.CONTAINS},
                'key': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
                'username': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
                'timestamp': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
                'description': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
            },
            loading: true,
		
        }
    },
  
    mounted() {
        fetch('https://wby808.deta.dev/draws/')
        .then((response) => { return response.json()})
        .then((jsonData) => { this.draws = jsonData});
        this.loading = false;
    }
    
}
</script>

<style lang="scss" scoped>
::v-deep(.p-paginator) {
    .p-paginator-current {
        margin-left: auto;
    }
}


::v-deep(.p-datatable.p-datatable-draws) {
    .p-datatable-header {
        padding: 1rem;
        text-align: left;
        font-size: 1.5rem;
    }

    .p-paginator {
        padding: 1rem;
    }

    .p-datatable-thead > tr > th {
        text-align: left;
    }

    .p-datatable-tbody > tr > td {
        cursor: auto;
    }

    .p-dropdown-label:not(.p-placeholder) {
        text-transform: uppercase;
    }
}
</style>