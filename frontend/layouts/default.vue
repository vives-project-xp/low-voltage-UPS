<template>
  <div class="h-screen flex flex-col">
    <!-- Navbar -->
    <AppHeader class="flex-none sticky top-0 left-0 right-0" />
    <!-- Page content -->
		<div class="flex-auto">
			<slot />
		</div>
    <!-- Footer -->
    <AppFooter class="flex-none p-4" />
  </div> 
</template>