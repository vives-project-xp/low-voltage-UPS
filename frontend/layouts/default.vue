<template>
    <div class="h-screen flex flex-col">
        <AppHeader class="flex-none sticky top-0 left-0 right-0 p-4"/>
        <div class="flex-auto">
            <slot />
        </div>
        <AppFooter class="flex-none p-4" />
    </div>
</template>