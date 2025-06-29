<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

interface Plume {
    plume_id: string;
    lat: number;
    lon: number;
    emission_auto: number | null;
    emission_uncertainty: number | null;
    datetime: string;
    gas: string;
    sector: string;
    platform: string;
    provider: string;
}

const props = defineProps<{ country: string }>()

const countryCenters: Record<string, [number, number]> = {
    'United States': [37.0902, -95.7129],
    'United Kingdom': [55.3781, -3.4360],
    'Switzerland': [46.8182, 8.2275],
    'Nigeria': [9.0820, 8.6753],
    'Ghana': [7.9465, -1.0232],
    'India': [20.5937, 78.9629],
    'Brazil': [-14.2350, -51.9253],
    'China': [35.8617, 104.1954],
    'Russia': [61.5240, 105.3188],
    'Romania': [45.9432, 24.9668],
    'Croatia': [45.1000, 15.2000],
    'Hungary': [47.1625, 19.5033],
    'Canada': [56.1304, -106.3468],
    'Germany': [51.1657, 10.4515],
    'France': [46.6034, 1.8883],
}

const map = ref<L.Map>()

onMounted(async () => {
    try {
        // Initialize map centered on selected country or default to Texas
        map.value = L.map('map').setView(countryCenters[props.country] || [31.5, -103.5], 6)
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map.value)

        console.log('🗺️ Map initialized, fetching plume data...')

        // Fetch plume data from API
        const res = await fetch('http://localhost:8001/v1/plumes/latest')
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`)
        }

        const data: Plume[] = await res.json()
        console.log('✅ Loaded plumes:', data.length)
        console.log('First plume:', data[0])

        if (data.length === 0) {
            console.warn('⚠️ No plume data available')
            return
        }

        // Add plumes to map
        data.forEach((plume: Plume, index: number) => {
            console.log(`🗺️ Adding plume ${index + 1}:`, plume.lat, plume.lon, plume.emission_auto)

            if (plume.lat && plume.lon) {
                // Create marker with enhanced visibility
                const emissionValue = plume.emission_auto || 0
                const color = emissionValue > 1000 ? '#dc2626' :
                    emissionValue > 500 ? '#ea580c' : '#f59e0b'

                const marker = L.circleMarker([plume.lat, plume.lon], {
                    radius: 15,
                    fillColor: color,
                    color: '#ffffff',
                    weight: 3,
                    opacity: 1,
                    fillOpacity: 0.8
                }).addTo(map.value!)
                // Add popup with plume information
                marker.bindPopup(`
                    <div class="bg-white rounded-lg shadow-lg p-4 min-w-[280px]">
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="text-lg font-bold text-gray-800">Methane Plume</h3>
                            <span class="badge badge-primary badge-sm">${plume.plume_id.slice(0, 8)}</span>
                        </div>
                        
                        <div class="space-y-2">
                            <div class="flex justify-between items-center">
                                <span class="text-sm font-medium text-gray-600">Emission Rate:</span>
                                <span class="badge ${emissionValue > 1000 ? 'badge-error' : emissionValue > 500 ? 'badge-warning' : 'badge-success'} font-bold">
                                    ${emissionValue.toFixed(1)} kg/hr
                                </span>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="text-sm font-medium text-gray-600">Gas Type:</span>
                                <span class="badge badge-accent">${plume.gas}</span>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="text-sm font-medium text-gray-600">Sector:</span>
                                <span class="text-sm text-gray-800">${plume.sector}</span>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="text-sm font-medium text-gray-600">Platform:</span>
                                <span class="text-sm text-gray-800">${plume.platform}</span>
                            </div>
                            
                            <div class="flex justify-between items-center">
                                <span class="text-sm font-medium text-gray-600">Date:</span>
                                <span class="text-xs text-gray-600">${new Date(plume.datetime).toLocaleDateString()}</span>
                            </div>
                        </div>
                    </div>
                `)
            }
        })

        console.log(`✅ Added ${data.length} plumes to map`)

    } catch (error) {
        console.error('❌ Error loading plume data:', error)
    }
})

watch(() => props.country, (newCountry, oldCountry) => {
    if (map.value && countryCenters[newCountry]) {
        map.value.flyTo(countryCenters[newCountry], 6, { animate: true, duration: 1.5 })
    }
})
</script>

<template>
    <div id="map" class="h-screen w-full"></div>
</template>