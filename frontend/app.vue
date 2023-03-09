<template>
  <div class="drawer drawer-end">
    <input id="my-drawer-3" type="checkbox" class="drawer-toggle" /> 
    <div class="drawer-content flex flex-col">
      <!-- Navbar -->
      <div class="flex-none sticky top-0 left-0 right-0 w-full navbar bg-base-300">
        <div class="flex-1 px-2 mx-2">Low Voltage UPS</div>
        <div class="flex-none hidden lg:block">
          <ul class="menu menu-horizontal">
            <!-- Navbar menu content here -->
            <li><NuxtLink to="/">Home</NuxtLink></li>
            <li><NuxtLink to="/setup">Setup</NuxtLink></li>
            <li><NuxtLink to="/about">About</NuxtLink></li>
            <li><NuxtLink to="/contact">Contact</NuxtLink></li>
          </ul>
        </div>
        <div class="flex-none lg:hidden">
          <label for="my-drawer-3" class="btn btn-square btn-ghost">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-6 h-6 stroke-current"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </label>
        </div>
      </div>
      <!-- Page content -->
      <NuxtPage class="flex-auto"/>
      <!-- Footer -->
      <footer class="footer footer-center flex-none p-4 bg-base-300 text-base-content">
        <div>
          <p>Copyright &copy; {{ new Date().getFullYear() }} - All right reserved by ?</p>
        </div>
      </footer>
    </div> 
    <!-- Sidebar -->
    <div class="drawer-side">
      <label for="my-drawer-3" class="drawer-overlay"></label> 
      <ul class="menu p-4 w-80 bg-base-100">
        <!-- Sidebar content -->
        <li><NuxtLink to="/">Home</NuxtLink></li>
        <li><NuxtLink to="/setup">Setup</NuxtLink></li>
        <li><NuxtLink to="/about">About</NuxtLink></li>
        <li><NuxtLink to="/contact">Contact</NuxtLink></li>
      </ul>
    </div>
  </div>
</template>
