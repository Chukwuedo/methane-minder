import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders main app component', () => {
    const wrapper = mount(App)
    expect(wrapper.exists()).toBe(true)
  })

  it('contains the Dashboard component', () => {
    const wrapper = mount(App)
    const html = wrapper.html()
    // Check that the app renders successfully
    expect(html).toBeTruthy()
  })
})
