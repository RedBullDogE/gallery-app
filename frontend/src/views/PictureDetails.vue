<template>
    <div class="picture-container" v-if="picture && !notFound">
        <router-link class="link" :to="{ name: 'Home' }"
            >Back to Home</router-link
        >

        <div class="picture-details">
            <img
                :src="`http://localhost:8000${picture.file}`"
                alt="Picture"
                draggable="false"
            />

            <div class="picture-details__info">
                <p class="picture-details__author">{{ picture.author }}</p>
                <p class="picture-details__desc">
                    {{ picture.description }}
                </p>
            </div>
        </div>
    </div>
    <div v-else>Page not found!</div>
</template>

<script>
export default {
    data() {
        return {
            notFound: false,
            picture: null,
        };
    },
    async mounted() {
        const id = this.$route.params.id;

        const response = await fetch(`http://localhost:8000/api/list/${id}/`, {
            method: "GET",
        });
        if (response.status == 404) {
            this.notFound = true;
        } else {
            this.picture = await response.json().then((data) => data.data);
        }
    },
};
</script>

<style lang="scss">
.picture-container {
    margin: 5rem auto;
    width: fit-content;

    .link {
        display: inline-block;
        box-shadow: 0 0.5rem 1rem lightskyblue;
        font-size: 1.4rem;
        padding: 1rem 2rem;
        margin: 1rem;
        transition: transform 0.2s;

        &:active {
            transform: translateY(3px);
        }
    }

    .picture-details {
        border-radius: 1rem;
        box-shadow: 0 0.8rem 2rem rgba(#111, 0.5);
        padding: 1.8rem 2rem;

        img {
            display: block;
            margin: 0 auto;
            max-width: 100rem;
            max-height: 80rem;
        }

        &__author {
            margin-top: 1rem;
            font-size: 1.6rem;
            font-weight: 600;
        }

        &__desc {
            font-size: 1.4rem;
        }
    }
}
</style>