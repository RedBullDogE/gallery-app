<template>
    <figure class="picture-card">
        <img
            @load="loaded"
            :src="`http://localhost:8000${picture.thumbnail}`"
            alt="Picture"
            draggable="false"
        />
    </figure>
</template>

<script>
export default {
    props: ["picture"],
    methods: {
        loaded() {
            this.$emit('pictureLoaded')
        }
    }
};
</script>

<style lang="scss">
.picture-card {
    overflow: hidden;

    img {
        cursor: pointer;
        width: 100%;
        height: 100%;
        max-height: 30rem;
        object-fit: cover;
    }
}
</style>