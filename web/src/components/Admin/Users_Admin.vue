<template>
    <div class="ui stackable grid vertically padded container">
        <div class="eight wide column">
            <div class="ui segment">
                <b-card bg-variant="success" text-variant="white" title="Administrator Panel: Users List" class="text-center" title-tag="h1">
                </b-card>
                <br><br>
                Here you can see all registered users, just click the username to expand it.
                <br><br><br>
                <table class="table table-hover justify-content-md-center">
                    <tr v-for="(user, index) in usernames" :key="index">
                        <b-card no-body class="mb-1">
                            <b-card-header header-tag="header" class="p-1" role="tab">
                                <b-button block v-b-toggle="'accordion-' + user.username" variant="info" @click="getInfo(user.username)">{{user.username}}</b-button>
                            </b-card-header>
                            <b-collapse :id="'accordion-' + user.username" accordion="my-accordion" role="tabpanel">
                                <b-card-text>
                                    Username: {{ user.username }}
                                    <br>
                                    Name: {{name}}
                                    <br>
                                    Surname: {{surname}}
                                    <br>
                                    Email: {{email}}
                                    <br>
                                    Topics: <span v-for="(topic, index) in topics" :key="index">{{ topic }};  </span>
                                </b-card-text>
                            </b-collapse>
                        </b-card>
                    </tr>
                </table>
                <br><br>
                <div class="btn-group-center" role="group">
                    <b-button
                    variant="warning"
                    size="lg"
                    @click="$router.go(-1)">
                    Back
                    </b-button>
                    <b-button
                    variant="success"
                    size="lg"
                    @click="$router.push('/home')">
                    Home
                    </b-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      usernames: [],
      name: '',
      surname: '',
      email: '',
      topics: [],

    };
  },
  methods: {
    fetchAuthenticatedUser() {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      
      axios.get('/account/me', config)
        .then((response) => {
          
          this.user = response.data.data;
          alert(user)
        });
    },
    getUsers() {
      const path = '/admin/users';
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      axios.get(path, config)
        .then((res) => {
          this.usernames = res.data.usernames;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getInfo(username) {
      const token = localStorage.getItem('auth-token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      const path = '/admin/users';
      const payload = { username };
      axios.post(path, payload, config)
        .then((res) => {
          this.name = res.data.name;
          this.surname = res.data.surname;
          this.email = res.data.email;
          this.topics = res.data.topics;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.fetchAuthenticatedUser();
    this.getUsers();
  },
};
</script>
