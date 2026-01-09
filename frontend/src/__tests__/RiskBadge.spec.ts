import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import RiskBadge from '../components/RiskBadge.vue'

describe('RiskBadge', () => {
  it('renders properly with low risk', () => {
    const wrapper = mount(RiskBadge, {
      props: {
        risk: 'low'
      }
    })
    expect(wrapper.html()).toBeTruthy()
    expect(wrapper.find('.badge').exists()).toBe(true)
  })

  it('renders properly with high risk', () => {
    const wrapper = mount(RiskBadge, {
      props: {
        risk: 'high'
      }
    })
    expect(wrapper.html()).toBeTruthy()
    expect(wrapper.find('.badge').exists()).toBe(true)
  })

  it('renders with unknown risk level', () => {
    const wrapper = mount(RiskBadge, {
      props: {
        risk: 'unknown'
      }
    })
    expect(wrapper.html()).toBeTruthy()
  })
})
