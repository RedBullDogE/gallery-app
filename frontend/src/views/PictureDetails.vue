<template>
    <div class="picture-container" v-if="picture && !notFound">
        <div class="picture-details">
            <img
                :src="`http://localhost:8000${picture.file}`"
                alt="Picture"
                draggable="false"
            />

            <div class="picture-details__info">
                <a
                    class="picture-details__edit"
                    v-if="editing.isAuthor && user"
                    @click="editing.isEdit = !editing.isEdit"
                    >Edit</a
                >
                <a
                    class="picture-details__delete"
                    v-if="editing.isAuthor && user"
                    @click="deletePicture"
                    >Delete</a
                >
                <p class="picture-details__author">
                    {{ picture.author }}
                    <span>({{ picture.pub_date | datetime }})</span>
                </p>
                <p class="picture-details__desc" v-if="!editing.isEdit">
                    {{ picture.description }}
                </p>
                <form class="picture-details__edit-form" method="post" v-else>
                    <textarea
                        name="description"
                        v-model.trim="editing.description"
                    ></textarea>
                    <button
                        class="edit-btn"
                        type="submit"
                        @click.prevent="updateDescription"
                    >
                        Change
                    </button>
                </form>
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
            editing: {
                isAuthor: false,
                isEdit: false,
                description: "",
            },
        };
    },
    props: ["user"],
    filters: {
        datetime(string) {
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            const datetime = string.split('T')         
            const dArr= datetime[0].split('-')
            const tArr = datetime[1].split('.')[0].split(':')

            return `${tArr[0]}:${tArr[1]} ${dArr[2]} ${months[dArr[1]-1]} ${dArr[0]}`
        }
    },
    async mounted() {
        const response = await this.getData();

        switch (response.status) {
            case 403: {
                const isRefreshed = await this.refresh();

                if (isRefreshed) {
                    const afterRefreshResponse = await this.getData();

                    const requestData = await afterRefreshResponse.json();
                    this.picture = requestData.data;
                    this.editing.isAuthor = requestData.isAuthor;
                }
                break;
            }
            case 404:
                this.notFound = true;
                break;
            case 200: {
                const requestData = await response.json();
                this.picture = requestData.data;
                this.editing.description = this.picture.description;
                this.editing.isAuthor = requestData.isAuthor;

                break;
            }
            default:
                console.log("Something went wrong with data requesting...");
        }
    },
    methods: {
        async getData() {
            const id = this.$route.params.id;

            const headers = this.user
                ? {
                      Authorization: `Bearer ${localStorage.getItem(
                          "accessToken"
                      )}`,
                      "Content-Type": "application/json",
                  }
                : {
                      "Content-Type": "application/json",
                  };

            return await fetch(`http://localhost:8000/api/list/${id}/`, {
                method: "GET",
                headers,
            });
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
                    this.$router.push({name: 'Login'})

                    break;
                case 200: {
                    const data = await response.json();
                    const newAccessToken = data.access;
                    localStorage.setItem("accessToken", newAccessToken);

                    return true;
                }
                default:
                    console.log("Something went wrong with refreshing..");
            }

            return false;
        },
        async updateDescription() {
            const id = this.picture.id;
            const access = localStorage.getItem("accessToken");

            const newDescription = this.editing.description;

            if (newDescription !== this.picture.description) {
                const response = await fetch(
                    `http://localhost:8000/api/update/${id}/`,
                    {
                        method: "POST",
                        headers: {
                            Authorization: `Bearer ${access}`,
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            description: newDescription,
                        }),
                    }
                );

                switch (response.status) {
                    case 403:
                        console.log("No permissions");
                        break;
                    case 200: {
                        const responseData = await response.json();

                        this.picture = responseData.data;
                        break;
                    }
                    default:
                        console.log(
                            "Something went wrong with updating data..."
                        );
                }
            }

            this.editing.isEdit = false;
        },
        async deletePicture() {
            if (confirm("Are u sure u wanna delete it?")) {
                const id = this.picture.id;
                const access = localStorage.getItem("accessToken");

                const response = await fetch(
                    `http://localhost:8000/api/delete/${id}/`,
                    {
                        method: "DELETE",
                        headers: {
                            Authorization: `Bearer ${access}`,
                            "Content-Type": "application/json",
                        },
                    }
                );

                switch (response.status) {
                    case 403:
                        console.log("No permissions");
                        break;
                    case 200: {
                        this.$router.push({ name: "Home" });
                        break;
                    }
                    default:
                        console.log(
                            "Something went wrong with deleting data..."
                        );
                }
            }
        },
    },
};
</script>

<style lang="scss">
.picture-container {
    margin: 5rem auto;
    width: fit-content;
    min-width: 50%;

    .picture-details {
        border-radius: 1rem;
        box-shadow: 0 0.8rem 2rem rgba(#111, 0.5);
        padding: 1.8rem 2rem;

        min-width: 50%;

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

            span {
                font-size: 1.4rem;
                font-weight: 300;
            }
        }

        &__desc {
            font-size: 1.4rem;
            white-space: pre-wrap;
        }

        &__edit,
        &__delete {
            font-size: 1.2rem;
            font-weight: 600;
            margin-right: 2rem;

            float: right;
            transition: color 0.2s;
            cursor: pointer;
        }

        &__edit:hover {
            color: lightseagreen;
        }

        &__delete:hover {
            color: lightcoral;
        }

        &__edit-form {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            margin: 1rem 0;

            textarea {
                font-family: "Open Sans", sans-serif;
                width: 50%;
                height: 10rem;
                resize: none;
                outline: none;

                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
            }

            .edit-btn {
                padding: 0.5rem 1.2rem;
                border-radius: 0.5rem;
                font-weight: 600;
                background-color: lightseagreen;
                color: #fff;

                border: 2px solid seagreen;

                margin-top: 1.5rem;

                box-shadow: 0 0.5rem 1.2rem #777;
                transition: transform 0.2s;

                &:active,
                &:focus {
                    transform: translateY(3px);
                    outline: none;
                }
            }
        }
    }
}
</style>