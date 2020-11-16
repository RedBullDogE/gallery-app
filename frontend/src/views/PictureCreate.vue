<template>
    <div class="add-picture">
        <form
            class="add-picture-form"
            @submit.prevent="submitForm"
            method="POST"
        >
            <h2>Add picture</h2>
            <p class="error" v-if="incorrectData">Inccorrect inputed data</p>

            <div class="form-group">
                <div class="form-group__input">
                    <label for="image">Picture</label>
                    <input
                        type="file"
                        name="image"
                        @change="loadFile($event)"
                        accept="image/png, image/jpeg"
                        @blur="$v.imageSrc.$touch()"
                    />
                </div>
                <img
                    :src="imageSrc"
                    alt="Uploaded picture"
                    class="uploaded-picture"
                    v-if="imageSrc"
                />
                <p
                    class="error"
                    v-if="$v.imageSrc.$dirty && !$v.imageSrc.required"
                >
                    This field is required
                </p>
            </div>

            <div class="form-group">
                <label for="description">
                    Description
                    <span :class="{ 'max-length': description.length >= 1000 }"
                        >({{ description.length }}/1000)
                    </span>
                </label>
                <textarea
                    class="description-input"
                    v-model="description"
                    name="description"
                    maxlength="1000"
                ></textarea>
            </div>

            <button type="submit">Add picture</button>
        </form>
    </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";

export default {
    data() {
        return {
            description: "",
            imageSrc: "",
            imageFile: null,
            incorrectData: false,
        };
    },
    validations: {
        imageSrc: {
            required,
        },
    },
    methods: {
        loadFile(event) {
            const reader = new FileReader();
            reader.onload = () => {
                this.imageSrc = reader.result;
            };

            const file = event.target.files[0];
            reader.readAsDataURL(file);
            this.imageFile = file;
        },
        async sendRequest() {
            const access = localStorage.getItem("accessToken");
            const formdata = new FormData();

            formdata.append("file", this.imageFile);
            formdata.append("description", this.description);

            return await fetch("http://127.0.0.1:8000/api/create/", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${access}`,
                },
                body: formdata,
            });
        },
        async submitForm() {
            this.$v.$touch();
            if (this.$v.$invalid) {
                this.incorrectData = true;
                return;
            }

            const response = await this.sendRequest();

            if (response.ok) {
                this.$router.push({ name: "Home" });
                return;
            }

            // Errors
            switch (response.status) {
                case 422:
                    this.incorrectData = true;
                    break;
                case 403: {
                    const isRefreshed = await this.refresh();

                    if (isRefreshed) {
                        this.submitForm();
                        return;
                    }
                    console.error("Refresh token has expired. Please, relogin");
                    break;
                }
                default:
                    console.error("Something goes wrong with request...");
            }
        },
        async refresh() {
            const access = localStorage.getItem("accessToken");
            const refresh = localStorage.getItem("refreshToken");

            const response = await fetch(
                "http://localhost:8000/api/token/refresh/",
                {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${access}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        refresh,
                    }),
                }
            );

            switch (response.status) {
                case 401:
                    localStorage.removeItem("user");
                    localStorage.removeItem("accessToken");
                    localStorage.removeItem("refreshToken");

                    break;
                case 200: {
                    const data = await response.json();
                    const newAccessToken = data.access;
                    localStorage.setItem("accessToken", newAccessToken);

                    return true;
                }
                default:
                    console.error("Something went wrong with refreshing..");
            }

            return false;
        },
    },
};
</script>

<style lang="scss">
.add-picture {
    margin: 2rem auto;
    display: flex;
    justify-content: center;

    .add-picture-form {
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
            display: flex;
            flex-direction: column;
            align-items: center;

            label {
                margin-right: 1rem;
                margin-bottom: 1rem;
            }

            &__input {
                padding: 0.5rem 1rem;
                transition: all 0.3s;
                border: 1px solid #111;
                border-radius: 3px;
                margin-bottom: 1rem;

                &:focus {
                    outline: none;
                    background-color: rgba(#ccc, 0.5);
                }
            }

            .uploaded-picture {
                text-align: center;
                margin: 0 auto;
                display: block;
                max-width: 60rem;
                max-height: 60rem;
            }

            .description-input {
                width: 80%;
                height: 15rem;
                resize: none;
                outline: none;

                font-family: "Open Sans", sans-serif;
                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
            }

            .max-length {
                color: red;
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