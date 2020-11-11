<template>
    <div id="app">
        <h1 class="app-title">Gallery App</h1>
        <router-view />
    </div>
</template>

<style lang="scss">
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 62.5%;
    font-family: 'Open Sans', sans-serif;
}

h1 {
    font-size: 4rem;
    font-weight: 800;
}

h2 {
    font-size: 2.6rem;
}

.app-title {
    margin: 1rem 3rem;
}
</style>
