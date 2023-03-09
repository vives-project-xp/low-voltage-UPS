<template>
    <div class="h-screen flex flex-col">
        <AppHeader class="flex-none sticky top-0 left-0 right-0 p-4 dark:bg-black dark:text-white"/>
        <div class="flex-auto dark:bg-black dark:text-white">
            <slot />
        </div>
        <AppFooter class="flex-none p-4 dark:bg-black dark:text-white" />
    </div>
</template>