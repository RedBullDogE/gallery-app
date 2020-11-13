<template>
    <div class="login">
        <form class="login-form" @submit.prevent="checkForm" method="POST">
            <h2>Login form</h2>
            <p class="error" v-if="incorrectCredentials">
                Inccorrect username or password
            </p>
            <div>
                <label for="username">Username</label>
                <input v-model="username" name="username" type="text" />
            </div>

            <div>
                <label for="password">Password</label>
                <input type="password" v-model="password" name="password" />
            </div>

            <button type="submit">Log In</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: "",
            password: "",
            incorrectCredentials: false,
        };
    },
    methods: {
        async checkForm() {
            if (this.username && this.password) {
                const userData = {
                    username: this.username,
                    password: this.password,
                };

                const response = await fetch(
                    "http://127.0.0.1:8000/api/token/",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(userData),
                    }
                );

                switch (response.status) {
                    case 401:
                        this.incorrectCredentials = true;

                        break;
                    case 200: {
                        const data = await response.json();

                        if (data.access && data.refresh) {
                            localStorage.setItem("accessToken", data.access);
                            localStorage.setItem("refreshToken", data.refresh);
                            localStorage.setItem("user", this.username);

                            this.$emit("login", this.username);

                            this.$router.push({ name: "Home" });
                        } else {
                            console.log("Something goes wrong with token...");
                        }

                        break;
                    }
                    default:
                        console.log("Something goes wrong with request...");
                }
            }
        },
    },
};
</script>

<style lang="scss">
.login {
    margin: 2rem auto;
    display: flex;
    justify-content: center;

    .login-form {
        padding: 2rem 3rem;
        border-radius: 1rem;
        box-shadow: 0 1rem 2rem rgba(#111, 0.5);
        font-size: 2rem;

        display: flex;
        flex-direction: column;
        align-items: center;

        div {
            margin: 1rem 0;

            label {
                margin-right: 1rem;
            }

            input {
                padding: 0.5rem 1rem;
                transition: all 0.3s;
                border: 1px solid #111;
                border-radius: 3px;

                &:focus {
                    outline: none;
                    background-color: rgba(#ccc, 0.5);
                }
            }
        }

        .error {
            font-size: 1.2rem;
            color: red;
            margin-top: 0.5rem;
        }

        button {
            font-size: 2rem;
            font-weight: 600;
            padding: 0.5rem 2rem;
        }
    }
}
</style>