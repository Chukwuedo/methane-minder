<template>
    <div class="card bg-base-100 shadow h-full w-full">
        <div class="card-body p-4 flex flex-col">
            <h3 class="card-title text-base mb-2">Methane Emissions</h3>
            <div class="flex-1 min-h-0">
                <Line :data="chartData" :options="chartOptions" :key="dataKey" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps<{ emissions: number[], years: number[] }>()

const dataKey = computed(() => `${props.emissions.length}-${props.years.length}`)

const chartData = computed(() => {
    console.log('📊 Chart data emissions:', props.emissions)
    console.log('📊 Chart data years:', props.years)
    return {
        labels: props.years,
        datasets: [{
            label: 'Methane Emissions (Million tCO₂eq)',
            data: props.emissions,
            borderColor: 'rgba(75,192,192,1)',
            backgroundColor: 'rgba(75,192,192,0.2)',
            tension: 0.4,
            pointBackgroundColor: 'rgba(75,192,192,1)',
            pointRadius: 4,
        }]
    }
})

const chartOptions = computed(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                usePointStyle: true, // Change rectangle to a small circle
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            min: 0,
            max: Math.max(...props.emissions) * 1.2, // Add 20% padding above max value
            ticks: {
                stepSize: Math.max(...props.emissions) / 5 // Divide range into 5 steps
            }
        }
    }
}))
</script>