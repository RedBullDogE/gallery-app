<template>
    <div class="home">
        <h2 class="home-title">HOME PAGE</h2>
        <div
            class="picture-grid"
            v-if="pictures.length"
            v-show="!loading.isLoading"
        >
            <PictureCard
                v-for="pic in pictures"
                :key="pic.id"
                :picture="pic"
                @pictureLoaded="loadListener"
                @click.native="
                    $router.push({ name: 'Details', params: { id: pic.id } })
                "
            />
        </div>

        <Loader v-if="loading.isLoading" :error="loading.error" />
    </div>
</template>

<script>
// @ is an alias to /src
import PictureCard from "@/components/PictureCard.vue";
import Loader from "@/components/Loader.vue";

export default {
    name: "Home",
    components: {
        PictureCard,
        Loader,
    },
    data() {
        return {
            currentPage: null,
            pageCount: null,
            pictures: [],
            loading: {
                loadedPictureCount: 0,
                isLoading: true,
                error: false,
            },
        };
    },
    methods: {
        loadListener() {
            this.loading.loadedPictureCount++;

            if (this.loading.loadedPictureCount >= this.pictures.length)
                this.loading.isLoading = false;
        },
    },
    async mounted() {
        setTimeout(() => {
            if (this.loading.isLoading) {
                this.loading.error = true;
            }
        }, 3000);

        const response = await fetch("http://127.0.0.1:8000/api/list/", {
            method: "GET",
        });

        const data = await response.json();

        this.currentPage = data.page;
        this.pageCount = data.pageCount;
        this.pictures = data.data;
    },
};
</script>

<style lang="scss">
.home {
    margin: 5rem 15rem;

    .home-title {
        text-align: center;
        margin-bottom: 2rem;
    }

    .picture-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(30rem, 1fr));
        grid-auto-rows: minmax(30rem, 1fr);
        grid-gap: 1.5rem;
    }
}
</style>
