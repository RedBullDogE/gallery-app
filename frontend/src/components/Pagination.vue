<template>
    <div class="pagination">
        <a @click="$emit('prev')">&laquo;</a>
        <a
            v-for="n in pageCount"
            :key="n"
            :class="{ active: n == currentPage }"
            @click="$emit('set-page', n)"
            >{{ n }}</a
        >
        <a @click="$emit('next')" class="next-btn">&raquo;</a>
    </div>
</template>

<script>
export default {
    props: ["pageCount", "currentPage"],
};
</script>

<style lang="scss">
.pagination {
    display: inline-block;
    margin: 2rem auto;

    & a {
        color: black;
        float: left;
        padding: 8px 16px;
        text-decoration: none;
        cursor: pointer;
        font-size: 1.6rem;
        border-radius: 5px;
        transition: background-color .3s;

        &.active {
            background-color: lightcoral;
            color: white;
        }
    }

    & a:hover:not(.active) {
        background-color: #ddd;
    }
}
</style>