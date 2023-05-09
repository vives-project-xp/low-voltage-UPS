<template>
  <div class="h-screen flex flex-col">
    <!-- Navbar -->
    <AppHeader class="flex-none sticky top-0 left-0 right-0 " />
    <!-- Page content -->
		<div class="flex-auto tertiary-color" style="background-image: linear-gradient(to right, #00b09b, #96c93d);">
      <div class="mx-auto max-w-5xl">
        <slot />
      </div>
		</div>
    <!-- Footer -->
    <AppFooter class="flex-none p-4" />
  </div> 
</template>