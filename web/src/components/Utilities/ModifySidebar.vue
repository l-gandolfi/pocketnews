<template>
    <div class="four wide column">
        <div>
        </div>
        <h4 class="ui horizontal divider header">
            Settings
        </h4>
        <div class="ui fluid vertical pointing menu">
            <div class="item">
                <router-link to="/settings/account">Account settings</router-link>
            </div>
            <div class="item">
                <router-link to="/settings/profile">Profile settings</router-link>
            </div>
            <div class="item">
                <router-link to="/settings/topics">Topic settings</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ModifySidebar",
    props: {
        user: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            news: ""
        }
    },
}
</script>