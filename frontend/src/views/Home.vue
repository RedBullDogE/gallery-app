<template>
    <div class="home">
        <div class="user-container">
            <p>{{ user || 'Anonymous'}}</p>
        </div>
        <h2 class="home-title">HOME PAGE</h2>
        <div class="home-content" v-show="!loading.isLoading">
            <div class="picture-grid" v-if="pictures.length">
                <PictureCard
                    v-for="pic in pictures"
                    :key="pic.id"
                    :picture="pic"
                    @pictureLoaded="loadListener"
                    @click.native="
                        $router.push({
                            name: 'Details',
                            params: { id: pic.id },
                        })
                    "
                />
            </div>

            <Pagination
                :pageCount="pageCount"
                :currentPage="currentPage"
                @next="nextPage"
                @prev="prevPage"
                @set-page="setPage"
            />
        </div>

        <Loader v-if="loading.isLoading" :error="loading.error" />
    </div>
</template>

<script>
import PictureCard from "@/components/PictureCard.vue";
import Loader from "@/components/Loader.vue";
import Pagination from "@/components/Pagination.vue";

export default {
    name: "Home",
    props: ['user'],
    components: {
        PictureCard,
        Loader,
        Pagination,
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
        async updateData(url) {
            this.loading.loadedPictureCount = 0;
            this.loading.isLoading = true;
            const response = await fetch(url, {
                method: "GET",
            });

            const data = await response.json();

            this.currentPage = data.page;
            this.pageCount = data.pageCount;
            this.pictures = data.data;
        },
        async prevPage() {
            if (this.currentPage > 1) {
                const newPage = this.currentPage - 1;
                this.$router.push({ name: "Home", query: { page: newPage } });
                await this.updateData(
                    `http://127.0.0.1:8000/api/list/?page=${newPage}`
                );
            }
        },
        async nextPage() {
            if (this.currentPage < this.pageCount) {
                const newPage = this.currentPage + 1;
                this.$router.push({ name: "Home", query: { page: newPage } });

                await this.updateData(
                    `http://127.0.0.1:8000/api/list/?page=${newPage}`
                );
            }
        },
        async setPage(page) {
            if (this.currentPage !== page) {
                this.$router
                    .push({ name: "Home", query: { page: page } })
                    .catch((err) => err);

                await this.updateData(
                    `http://127.0.0.1:8000/api/list/?page=${page}`
                );
            }
        },
    },
    async mounted() {
        const page = this.$route.query.page;
        setTimeout(() => {
            if (this.loading.isLoading && this.pictures.length) {
                this.loading.error = true;
            }
        }, 5000);

        const url = page
            ? `http://127.0.0.1:8000/api/list/?page=${page}`
            : "http://127.0.0.1:8000/api/list/";

        const response = await fetch(url, {
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
    margin: 5rem auto;
    width: 80%;
    max-width: 120rem;

    .user-container {
        display: flex;
        justify-content: flex-end;
        font-size: 2rem;

        p {
            margin: 0 2rem;
        }
    }

    .home-title {
        text-align: center;
        margin-bottom: 2rem;
    }

    .home-content {
        display: flex;
        justify-content: center;
        flex-direction: column;
        .picture-grid {
            display: grid;
            margin: 0 10rem;
            grid-template-columns: repeat(auto-fit, minmax(30rem, 1fr));
            grid-auto-rows: minmax(30rem, 1fr);
            grid-gap: 2rem;
        }
    }
}
</style>
