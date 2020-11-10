<template>
    <div class="loading-container">
        <div class="loader"></div>
        <div class="error-message" v-if="error">
            Something goes wrong ;( Please, reload the page
        </div>
    </div>
</template>

<script>
export default {
    props: ['error'],
}
</script>

<style lang="scss">
.loading-container {
    .loader {
        margin: 5rem auto;
        border: 1rem solid #f3f3f3; /* Light grey */
        border-top: 1rem solid #3498db; /* Blue */
        border-radius: 50%;
        width: 7rem;
        height: 7rem;
        animation: spin 0.7s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .error-message {
        font-size: 3rem;
        color: orangered;
        text-align: center;
    }
}
</style>