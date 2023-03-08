<template>
  <div>
    <select class="primary-color" v-model="$colorMode.preference"> 
      <option value="unknown" hidden="true">...</option> 
      <option value="system">System</option>      
      <option value="light">Light</option>      
      <option value="dark">dark</option>         
    </select>
  </div>
</template>