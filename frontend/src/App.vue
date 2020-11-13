<template>
    <div id="app">
        <h1 class="app-title">Gallery App</h1>
        <div class="auth-container">
            <p class="username" v-if="user">{{ user }}</p>
            <router-link :to="{ name: 'Login' }" class="login" v-if="!user"
                >Login</router-link
            >
            <a href="#" class="logout" @click="logout" v-else>Logout</a>
            <a href="#" class="signin" v-if="!user">Sign In</a>
        </div>
        <div class="user-container"></div>
        <router-view @login="login" :user="user" />
    </div>
</template>

<script>
export default {
    data() {
        return {
            user: null,
        };
    },
    methods: {
        login(username) {
            this.user = username;
        },
        logout() {
            this.user = null;
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            localStorage.removeItem("user");
        },
    },
    mounted() {
        const user = localStorage.getItem("user");

        if (user) {
            // const access = localStorage.getItem("accessToken"),
            // refresh = localStorage.getItem("refreshToken");

            this.user = user;
        }
    },
};
</script>

<style lang="scss">
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 62.5%;
    font-family: "Open Sans", sans-serif;
}

h1 {
    font-size: 4rem;
    font-weight: 800;
}

h2 {
    font-size: 2.6rem;
}

#app {
    margin: 2rem;

    .app-title {
        margin: 1rem 3rem;
    }

    .auth-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin: 0 5rem;

        a {
            font-size: 2rem;
            text-decoration: none;
            margin-right: 2rem;
            padding: 0.5rem 1.2rem;
            border-radius: 0.5rem;
            box-shadow: 0 0.5rem 2rem rgba(blueviolet, 0.6);
            transition: transform 0.2s;

            &:active {
                transform: translateY(2px);
            }
        }
    }

    .username {
        font-size: 2rem;
        margin: 0 3rem;
        font-weight: 600;

        padding: .5rem 1.5rem;
        background-color: lightseagreen;
        border-radius: 0.5rem;
        box-shadow: 0 0.5rem 2rem rgba(blueviolet, 0.6);

        color: #fff;
    }
}
</style>
