<template>
    <div class="flex flex-col lg:flex-row h-screen w-screen bg-base-200">
        <!-- Sidebar -->
        <div
            class="flex flex-col w-full lg:w-[30rem] lg:h-full h-auto bg-base-100 border-base-300 border-b lg:border-r lg:border-b-0">
            <!-- Header -->
            <div class="navbar sticky top-0 z-10 bg-primary text-primary-content px-6 py-4 w-full">
                <div class="flex-1">
                    <span class="text-xl sm:text-2xl font-bold">Methane Minder Dashboard</span>
                </div>
                <div class="flex-none flex items-center gap-2">
                    <label class="text-sm font-medium hidden sm:inline">Country:</label>
                    <select v-model="selectedCountry"
                        class="select select-bordered select-sm w-auto max-w-[150px] bg-white text-black">
                        <option>United States</option>
                        <option>United Kingdom</option>
                        <option>Switzerland</option>
                        <option>Nigeria</option>
                        <option>Ghana</option>
                        <option>India</option>
                        <option>Brazil</option>
                        <option>China</option>
                        <option>Russia</option>
                        <option>Romania</option>
                        <option>Croatia</option>
                        <option>Hungary</option>
                        <option>Canada</option>
                        <option>Germany</option>
                        <option>France</option>
                    </select>
                    <!-- Theme Toggle Switch -->
                    <button @click="$emit('toggle-theme')" class="btn btn-sm btn-outline">Toggle Theme</button>
                </div>
            </div>

            <!-- Stats Cards -->
            <div class="p-4 space-y-4 flex-shrink-0 w-full">
                <div class="card bg-base-200 shadow w-full">
                    <div class="card-body p-4">
                        <h3 class="card-title text-sm mb-2">Risk Assessment</h3>
                        <RiskBadge v-if="riskData" :risk="riskData.risk" />
                        <div v-if="error" class="alert alert-error mt-2">
                            <span class="text-xs">{{ error }}</span>
                        </div>
                        <p class="text-xs text-base-content/70 mt-2">{{ selectedCountry }}</p>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-2 w-full">
                    <div class="card bg-base-100 shadow w-full">
                        <div class="card-body p-3">
                            <h4 class="text-xs font-medium text-blue-600">Forecast</h4>
                            <p class="text-sm font-bold text-blue-800">
                                {{ riskData?.forecast ? (riskData.forecast / 1_000_000).toFixed(2) : '---' }} M
                            </p>
                            <p class="text-xs text-blue-600">t CO₂eq Projected</p>
                        </div>
                    </div>
                    <div class="card bg-base-100 shadow w-full">
                        <div class="card-body p-3">
                            <h4 class="text-xs font-medium text-green-600">Baseline</h4>
                            <p class="text-sm font-bold text-green-800">
                                {{ riskData?.baseline ? (riskData.baseline / 1_000_000).toFixed(2) : '---' }} M
                            </p>
                            <p class="text-xs text-green-600">t CO₂eq Historical</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Chart -->
            <div class="flex-1 p-4 overflow-hidden min-h-0 flex flex-col w-full">
                <div class="card bg-base-200 shadow h-full w-full">
                    <div class="card-body p-4 h-full flex flex-col">
                        <h3 class="card-title text-sm mb-2 flex-shrink-0">Historical Emissions</h3>
                        <div class="flex-1 min-h-0 w-full">
                            <EmissionChart v-if="chartData.emissions.length > 0" :emissions="chartData.emissions"
                                :years="chartData.years" />
                            <div v-else class="flex items-center justify-center h-full text-base-content/50">
                                <span class="text-sm">Loading chart...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="flex-1 w-full h-[60vh] lg:h-full">
            <MapView :country="selectedCountry" class="h-full w-full" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import MapView from './MapView.vue'
import EmissionChart from './EmissionChart.vue'
import RiskBadge from './RiskBadge.vue'

defineProps<{
    theme: string
}>()

defineEmits(['toggle-theme'])

interface RiskData {
    risk: string
    forecast: number
    baseline: number
}

interface ChartData {
    emissions: number[]
    years: number[]
}

const selectedCountry = ref('United States')
const riskData = ref<RiskData | null>(null)
const error = ref('')
const chartData = ref<ChartData>({ emissions: [], years: [] })

const fetchRiskData = async () => {
    try {
        error.value = ''
        const response = await fetch(`/v1/risk/${selectedCountry.value}`)
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
        riskData.value = await response.json()
    } catch (err) {
        error.value = 'Failed to fetch risk assessment data'
        console.error('Risk data fetch error:', err)
    }
}

const loadEmissionData = async () => {
    try {
        const csvUrl = import.meta.env.BASE_URL + 'methane-emissions.csv'
        const res = await fetch(csvUrl)
        if (!res.ok) throw new Error(`CSV load error: ${res.status}`)
        const csvText = await res.text()
        const lines = csvText.trim().split('\n')
        const headers = lines[0].split(',')
        const data = lines.slice(1).map(line => {
            const values = line.split(',')
            return headers.reduce((obj, key, idx) => ({ ...obj, [key]: values[idx] }), {} as Record<string, string>)
        })

        const countryRows = data.filter(row => row.Entity === selectedCountry.value)

        if (countryRows.length > 0) {
            chartData.value = {
                years: countryRows.map(row => Number(row.Year)),
                emissions: countryRows.map(row => Number(row.annual_emissions_ch4_total_co2eq) / 1_000_000)
            }
        } else {
            chartData.value = { emissions: [], years: [] }
        }
    } catch (err) {
        console.error('Chart data loading error:', err)
        chartData.value = { emissions: [], years: [] }
    }
}

watch(selectedCountry, () => {
    fetchRiskData()
    loadEmissionData()
})

onMounted(() => {
    fetchRiskData()
    loadEmissionData()
})
</script>
