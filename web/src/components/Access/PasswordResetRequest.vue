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
                  title="PockeNews - Reset the Password"
                >
                <br>
                </b-card>
              </div>
            </v-container>
          </div>
          <form v-on:submit.prevent="reset">
          <alert :message=message v-if="showMessage"></alert>
          <alertFail :message=message v-if="showFailMessage"></alertFail>
          <div class="container">
              <h2> Insert the email address that you use to access into PocketNews </h2>
              <br>
              <div class="row justify-content-md-center">
                  <div class="col-md-6">
                     <div class="form-group">
                          <input type="email" v-model="email" class="form-control" name="email" placeholder="Enter Email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required/>
                          <div class="invalid-feedback feedback-pos">
                            Please input valid email ID
                          </div>
                      </div>
                  </div>
              </div>
          </div>
            <button type="submit" class="btn btn-info" value="validate">Resend</button>
          </form>
          <br>
          <div class="border-top pt-3">
            <small class="text-muted">
             Need an account? <a class="ml-2" href="/registration">Sign Up Now</a> 
            </small>
          </div>
        </v-flex>
      </v-layout>
    </div>
  </div>

</template>


<script>
import axios from 'axios'
import Alert from '../Utilities/AlertSucc.vue';
import AlertFail from '../Utilities/AlertFail.vue';

export default {
  data () {
    return {
      email: '',
      showMessage: false,
      showFailMessage: false,
      message: '',
      allOk: false,
    }
  },
  components: {
    alert: Alert,
    alertFail: AlertFail,
  },
  methods: {
    reset() {
        const path = '/reset_psw';

        this.showMessage = false;
        this.showFailMessage = false;

        const payload = {
          email: this.email,
          op_id: 0,
        };


        axios.post(path, payload)
          .then((res) => {
            if (res.data.status == 'success') {
              this.message = "Hi "+res.data.user+"! A email with password reset instructions has been sent to your email adress!";
              this.showMessage = true;
              document.getElementById('email').value = "";
            } else {
              this.message = "No one account is recorded with this email. Are you sure about your pocketNews subscription?";
              this.showFailMessage = true;
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