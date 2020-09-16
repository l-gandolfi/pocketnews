<template>
  <div class="container">
    <div class="row justify-content-md-center">
      <v-layout align-center justify-center>
        <v-flex lg6>
          <div class="col-20 justify-content-md-center">
            <v-container fill-height>
              <div>
                <b-card
                  overlay
                  img-src="https://picsum.photos/900/250/?image=13"
                  img-alt="Card Image"
                  text-variant="black"
                  title="Now you can change your password!"
                >
                <br>
                </b-card>
              </div>
              <br><br>
              <h3>Please insert your new password and confirm it!</h3>
              <br>
              <br><br>
            </v-container>
          </div>
          <form v-on:submit.prevent="register" oninput='conf_password.setCustomValidity(conf_password.value != password.value ? "Passwords do not match." : "")'>
          <alert :message=message v-if="showDangerMessage"></alert>
          <div class="container">
              <div class="row">
                  <div class="col-md-6">
                     <div class="form-group">
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
                          <input type="password" v-model="conf_password" class="form-control" name="conf_password" placeholder="Confirm password" required />
                      </div>
                  </div>
              </div>
          </div>
            <button type="submit" class="btn btn-info" value="validate"> Confirm </button>
          </form>
          <br>
        </v-flex>
      </v-layout>
    </div>
  </div>

</template>


<script>
import axios from 'axios'
import Alert from '../Utilities/AlertSucc';

export default {
  computed: {
      nameState() {
        var controllo = this.password.length > 5 ? true : false;
        if (this.password.length == 0) controllo = null;
        return controllo;
      },
    },
  data () {
    return {
      password: '',
      message: '',
      showMessage: false,
      user_id: '',
    }
  },
  components: {
    alert: Alert,
  },
  methods: {
  register() {
        const path = '/reset_psw';

        this.showMessage = false;

        const payload = {
          password: this.password,
          op_id: 1,
          user_id: this.user_id,
        };

        axios.post(path, payload)
          .then((res) => {
            if (res.data.status == 'success') {
              alert('           New password set!         \nNow you will redirect to login page.')
              this.$router.push('/login');
            } else {
              alert('     You have already changed the password!      \n     Now you will redirect to login page.')
              this.$router.push('/login');
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
    check_validity() {
      const path = '/reset_psw';
      const payload = {
          op_id: 2,
          user_id: this.user_id,
        };
      axios.post(path, payload)
        .then((res) => {
          if (res.data.status == 'fail') {
            alert('The request is expired! Get another one!')
            this.$router.push('/passwordResetRequest');
          } 
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      
    }
  },
  created() {
      this.user_id = this.$route.params.user_id;
      this.check_validity();
  },
};
</script>