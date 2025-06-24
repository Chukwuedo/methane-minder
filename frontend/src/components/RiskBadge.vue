<template>
    <div class="flex items-center gap-2">
        <div class="badge badge-lg font-bold" :class="badgeClass">
            {{ displayRisk }}
        </div>
        <div class="text-xs text-base-content/70">
            {{ riskDescription }}
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    risk: string
}>()

const badgeClass = computed(() => {
    switch (props.risk?.toLowerCase()) {
        case 'high':
            return 'badge-error'
        case 'medium':
            return 'badge-warning'
        case 'low':
            return 'badge-success'
        default:
            return 'badge-ghost'
    }
})

const displayRisk = computed(() => {
    return props.risk?.charAt(0).toUpperCase() + props.risk?.slice(1) || 'Unknown'
})

const riskDescription = computed(() => {
    switch (props.risk?.toLowerCase()) {
        case 'high':
            return 'Immediate attention required'
        case 'medium':
            return 'Monitor closely'
        case 'low':
            return 'Within acceptable range'
        default:
            return 'Assessment unavailable'
    }
})
</script>