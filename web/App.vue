<script setup>
import { RouterLink, RouterView } from 'vue-router'

const theme = {
  token: {
    colorPrimary: '#1f1f1f',
    colorPrimaryHover: '#2b2b2b',
    colorPrimaryActive: '#000000',
    colorPrimaryBg: '#5e5e5e',
    colorPrimaryBgHover: '#525252',
    colorPrimaryBorder: '#454545',
    colorPrimaryBorderHover: '#383838',
    colorPrimaryText: '#1f1f1f',
    colorPrimaryTextHover: '#2b2b2b',
    colorPrimaryTextActive: '#000000',

    colorBgBase: '#f5f5f5',
    colorBgContainer: '#ffffff',
    colorBorder: '#d9d9d9',
    colorText: '#1f1f1f',
    colorTextSecondary: '#595959',
    colorLink: '#1f1f1f',
    colorLinkHover: '#2b2b2b',
    colorLinkActive: '#000000',
    borderRadius: 4,
  },
}
</script>

<template>
  <a-config-provider :theme="theme">
    <router-view />
  </a-config-provider>
</template>

<style scoped></style>
