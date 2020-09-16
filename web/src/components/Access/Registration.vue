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
                      <h3>Join in PocketNews! Is free, easy and fast!</h3>
                    </b-card-text>
                    </b-card>          
                </div>
                <br><br>
                <h3>Please insert your data</h3>
                <br>
                All field below are mandatory, fill them!
                <br><br>
                <form v-on:submit.prevent="register" oninput='conf_password.setCustomValidity(conf_password.value != password.value ? "Passwords do not match." : "")'>
                <alert :message=message v-if="showDangerMessage"></alert>
                <div class="container">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <h6>First name</h6>
                                <input type="text" v-model="first_name" class="form-control" name="first_name" placeholder="Enter first name" required/>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="form-group">
                              <h6>Last name</h6>
                              <input type="text" v-model="last_name" class="form-control" name="last_name" placeholder="Enter last name" required/>
                            </div>
                        </div>
                        
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <h6>Username</h6>
                                <input type="text" v-model="username" class="form-control" name="username" placeholder="Enter username" required/>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <h6>Email</h6>
                                <input type="email" label="Email" v-model="email" class="form-control" name="email" placeholder="Enter email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required/>
                                <div class="invalid-feedback feedback-pos">
                                  Please input valid email ID
                                </div>
                            </div> 
                        </div>      
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                          <div class="form-group">
                                <h6>Password</h6>
                                <b-form-input
                                  id="password"
                                  type="password" 
                                  class="form-control" 
                                  name="password" 
                                  placeholder="Enter Password"
                                  v-model="password"
                                  required 
                                  :state="nameState"
                                  aria-describedby="input-live-help input-live-feedback"/>
                                <b-form-invalid-feedback id="input-live-feedback">
                                  Enter at least 6 characters.
                                </b-form-invalid-feedback>
                                <b-form-text id="input-live-help">
                                  Long password are difficult to hack.
                                </b-form-text>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">      
                                <h6>Confirm password</h6>                
                                <input type="password" v-model="conf_password" class="form-control" name="conf_password" placeholder="Enter confirm password" required />
                            </div>
                        </div>
                    </div>
                </div>
                  <button type="submit" class="btn btn-info" value="validate" :disabled="!globalState"> Register </button>
                </form>
                <br>
                <div class="border-top pt-3">
                  <small class="text-muted">
                    Already Have An Account? <a class="ml-2" href="/login">Sign In</a>
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
  computed: {
    nameState() {
      let controllo = this.password.length > 5;
      if (this.password.length == 0) controllo = null;
      return controllo;
    },
    globalState() {
      const global = this.nameState == true && this.first_name.length > 0
          && this.last_name.length > 0 && this.email.length > 0 && this.username.length > 0;
      return global;
    },
    beforeRouteEnter(to, from, next) {
      const token = localStorage.getItem('auth-token');

      return token ? next('/') : next();
    },
  },
  data() {
    return {
      first_name: '',
      last_name: '',
      email: '',
      username: '',
      password: '',
      showDangerMessage: false,
      message: '',
      allOk: false,

    };
  },
  beforeRouteEnter(to, from, next) {
    const token = localStorage.getItem('auth-token');
    return token ? next('/') : next();
  },
  components: {
    alert: Alert,
  },
  methods: {
    register() {
      const path = '/register';

      this.showDangerMessage = false;

      const payload = {
        name: this.first_name,
        surname: this.last_name,
        email: this.email,
        username: this.username,
        password: this.password,
      };

        axios.post(path, payload)
          .then((res) => {
            if (res.data.status == 'fail') {
              this.message = "In the system it exists already a user with this "+ res.data.reason;
              this.showDangerMessage = true;
            } else {
              this.allOk = true;
              // save token in localstorage
              //localStorage.setItem('auth-token', res.data.data.access_token);
              // redirect
              this.$router.push('/waitConfirm/'+res.data.user_id);
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
