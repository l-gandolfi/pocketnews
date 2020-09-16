<template>
    <div class="ui stackable grid vertically padded container">
        <div class="sixteen wide column">
            <div class="ui segment">
              <div>
                <b-card
                  overlay
                  img-src="https://i.picsum.photos/id/2/650/250.jpg"
                  img-alt="Card Image"
                  text-variant="white"
                  >
                  <b-card-text>
                    <h1>PocketNews</h1>
                  </b-card-text>
                </b-card>
              </div>
              <br><br>
                <h3>Log in</h3>
                <br>
                Please insert your data
              <br><br>
              <form v-on:submit.prevent="login">
              <alert :message=message v-if="showDangerMessage"></alert>
              <div class="container">
                  <div class="row">
                      <div class="col-md-6">
                        <div class="form-group">
                              <h6>Email</h6>
                              <input type="email" v-model="email" class="form-control" name="email" placeholder="Enter Email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required/>
                              <div class="invalid-feedback feedback-pos">
                                Please input valid email ID
                              </div>
                          </div>
                      </div>
                      <div class="col-md-6">
                          <div class="form-group">
                              <h6>Password</h6>
                              <input type="password" v-model="password" class="form-control" name="password" placeholder="Enter password" required />
                          </div>
                      </div>
                  </div>
              </div>
                <button type="submit" class="btn btn-info" value="validate"> Login </button>
              </form>
              <br>
              <div class="border-top pt-3">
                <small class="text-muted">
                Need an account? <a class="ml-2" href="/registration">Sign Up Now</a>
                <br>
                <a class="ml-2" href="/passwordResetRequest">Forgot the password?</a>
                </small>
              </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios';
import Alert from '../Utilities/Alert.vue';

export default {
  data() {
    return {
      email: '',
      password: '',
      remember_flag: false,
      showDangerMessage: false,
      message: '',
      allOk: false,
    };
  },
  components: {
    alert: Alert,
  },
  beforeRouteEnter(to, from, next) {
    const token = localStorage.getItem('auth-token');
    return token ? next('/') : next();
  },
  methods: {
    login() {
        const path = '/login';

      this.showDangerMessage = false;

      const payload = {
        email: this.email,
        password: this.password,
        remember_flag: this.remember_flag,
      };

        axios.post(path, payload)
          .then((res) => {
            if (res.data.status == 'fail') {
              this.message = res.data.reason;
              this.showDangerMessage = true;
            } else if (res.data.status == 'warning'){
              //localStorage.setItem("login-token", res.data.token)
              this.allOk = true;
              this.$router.push('/waitConfirm/'+res.data.user_id);
            } else {
              this.allOk = true;
              localStorage.setItem('auth-token', res.data.data.access_token);
              if (res.data.topic == 0){
                this.$router.push('/topics');
                localStorage.setItem('topic', '0');
                localStorage.setItem('inTopic', '0');
              } else {
                this.$router.push('/home');
                localStorage.setItem('topic', '1');
              }
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
        });
    },
  },
};
</script>
