<template>
    <div id="app">
        <h1 class="app-title">Gallery App</h1>
        <div class="auth-panel">
            <router-link
                :to="{ name: 'Home' }"
                class="home-btn"
                v-if="$route.name !== 'Home'"
            >
                Home
            </router-link>

            <template v-if="user">
                <router-link :to="{ name: 'Create' }" class="add-picture-btn">
                </router-link>
                <p class="username">{{ user }}</p>
                <a href="#" class="logout" @click="logout">Logout</a>
            </template>
            
            <template v-else>
                <router-link
                    :to="{ name: 'Login' }"
                    class="login-btn"
                    v-if="!user"
                >
                    Login
                </router-link>
                <router-link
                    :to="{ name: 'Register' }"
                    class="register-btn"
                    v-if="!user"
                >
                    Sign In
                </router-link>
            </template>
        </div>
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

    .auth-panel {
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

        .home-btn {
            margin-right: auto;
            margin-left: 2rem;
        }

        .username {
            font-size: 2rem;
            margin-right: 2rem;
            font-weight: 600;

            padding: 0.5rem 1.5rem;
            background-color: lightseagreen;
            border-radius: 0.5rem;
            box-shadow: 0 0.5rem 2rem rgba(blueviolet, 0.6);

            color: #fff;
        }

        .add-picture-btn {
            position: relative;
            display: inline-block;
            font-size: 3.5rem;
            border-radius: 50%;
            width: 5rem;
            height: 5rem;
            background-color: lightseagreen;

            &:before,
            &:after {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: white;
            }

            &:before {
                width: 0.3rem;
                margin: 1.2rem auto;
            }
            &:after {
                margin: auto 1.2rem;
                height: 0.3rem;
            }
        }
    }
}
</style>
