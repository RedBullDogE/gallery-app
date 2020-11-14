<template>
    <div class="register-container">
        <form class="register-form" @submit.prevent="submitForm" method="POST">
            <h2>Register</h2>
            <p class="error" v-if="incorrectFormData">
                Inccorrect form data
            </p>
            <p class="error" v-if="userAlreadyExists">
                User with such username already exists
            </p>
            <div class="form-group">
                <div class="form-group__input">
                    <label for="username">Username</label>
                    <input
                        v-model="username"
                        name="username"
                        type="text"
                        @blur="$v.username.$touch()"
                    />
                </div>
                <p
                    class="error"
                    v-if="$v.username.$dirty && !$v.username.required"
                >
                    This field is required
                </p>
                <p
                    class="error"
                    v-if="$v.username.$dirty && !$v.username.minLength"
                >
                    Username must be equal or longer than 4 characters
                </p>
            </div>

            <div class="form-group">
                <div class="form-group__input">
                    <label for="email">Email</label>
                    <input
                        v-model="email"
                        name="email"
                        type="email"
                        @blur="$v.email.$touch()"
                    />
                </div>

                <p class="error" v-if="$v.email.$dirty && !$v.email.required">
                    This field is required
                </p>
                <p class="error" v-if="$v.email.$dirty && !$v.email.email">
                    Uncorrect email
                </p>
            </div>

            <div class="form-group">
                <div class="form-group__input">
                    <label for="password">Password</label>
                    <input
                        v-model="password"
                        name="password"
                        type="password"
                        @blur="$v.password.$touch()"
                    />
                </div>
                <p
                    class="error"
                    v-if="$v.password.$dirty && !$v.password.required"
                >
                    This field is required
                </p>
                <p
                    class="error"
                    v-if="$v.password.$dirty && !$v.password.minLength"
                >
                    Password must not be shorter than 6 characters
                </p>
            </div>

            <div class="form-group">
                <div class="form-group__input">
                    <label for="passwordConfirm">Confirm Password</label>
                    <input
                        type="password"
                        v-model="passwordConfirm"
                        name="passwordConfirm"
                        @blur="$v.passwordConfirm.$touch()"
                    />
                </div>
                <p
                    class="error"
                    v-if="
                        $v.passwordConfirm.$dirty &&
                        !$v.passwordConfirm.required
                    "
                >
                    This field is required
                </p>
                <p
                    class="error"
                    v-if="
                        $v.passwordConfirm.$dirty && !$v.passwordConfirm.sameAs
                    "
                >
                    Passwords do not match
                </p>
            </div>

            <button type="submit">Sign In</button>
        </form>
    </div>
</template>

<script>
import { required, minLength, sameAs, email } from "vuelidate/lib/validators";

export default {
    data() {
        return {
            username: "",
            email: "",
            password: "",
            passwordConfirm: "",
            incorrectFormData: false,
            userAlreadyExists: false
        };
    },
    validations: {
        username: {
            required,
            minLength: minLength(4),
        },
        email: {
            required,
            email,
        },
        password: {
            required,
            minLength: minLength(6),
        },
        passwordConfirm: {
            required,
            sameAs: sameAs("password"),
        },
    },
    methods: {
        async submitForm() {
            this.$v.$touch();

            if (this.$v.$invalid) {
                this.incorrectFormData = true;
                return;
            }
            // Clearing errors
            this.incorrectFormData = false;
            this.userAlreadyExists = false;


            const userData = {
                username: this.username,
                email: this.email,
                password: this.password
            }
            console.log(userData);

            const response = await fetch("http://127.0.0.1:8000/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            switch (response.status) {
                case 422:
                    this.incorrectFormData = true;

                    break;
                case 409:
                    this.userAlreadyExists = true;
                    
                    break;
                case 201: {
                    console.log('Successfuly registered!');
                    this.$router.push({ name: 'Login' })
                    break;
                }
                default:
                    console.log("Something goes wrong with register...");
            }
        },
    },
};
</script>

<style lang="scss">
.register-container {
    margin: 2rem auto;
    display: flex;
    justify-content: center;

    .register-form {
        padding: 2rem 3rem;
        border-radius: 1rem;
        box-shadow: 0 1rem 2rem rgba(#111, 0.5);
        font-size: 2rem;

        display: flex;
        flex-direction: column;
        align-items: center;

        .form-group {
            margin: 1rem 0;
            width: 100%;

            &__input {
                display: flex;
                justify-content: space-between;
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