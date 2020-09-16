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
                  img-src="https://picsum.photos/900/250/?image=19"
                  img-alt="Card Image"
                  text-variant="white"
                  title="PockeNews - Confirm your email!"
                >
                <br>
                </b-card>
              </div>
            </v-container>
          </div>
          <form v-on:submit.prevent="resend">
          <alert :message=message v-if="showMessage"></alert>
          <alert_fail :message=message v-if="showFailMessage"></alert_fail>
          <div class="container">
              <h2> A email has been sent to your email address, if you can't see it check spam box!</h2>
              <br>
              <p>If you didn't receive any email, please insert a new one address</p>
              <div class="row justify-content-md-center">
                  <div class="col-md-6">
                     <div class="form-group">
                          <input type="email" v-model="resend_email" class="form-control" name="resend_email" placeholder="Enter Email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required/>
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
        </v-flex>
      </v-layout>
    </div>
  </div>

</template>


<script>
import axios from 'axios'
import Alert from '../Utilities/AlertSucc.vue';
import AlertFail from '../Utilities/AlertFail.vue'

export default {
  data () {
    return {
      email: '',
      showMessage: false,
      message: '',
      showFailMessage: false,
      user_id: '',

    }
  },
  components: {
    alert: Alert,
    alert_fail: AlertFail,
  },
  methods: {
    resend() {
        const path = '/resend_email';

        this.showMessage = false;
        this.showFailMessage = false;

        const payload = {
          email: this.resend_email,
          user_id: this.user_id,
        };

        axios.post(path, payload)
          .then((res) => {
            if (res.data.status == 'success') {
              this.message = "A new email has been sent";
              this.showMessage = true;
            } else {
              this.showFailMessage = true;
              this.message = res.data.reason;
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      check_confirm() {
        const path = '/mail_checked';

        const payload = {
          user_id: this.user_id,
          op_id: 1,
        };
        axios.post(path, payload)
          .then((res) => {
            if (res.data.status == '13' || res.data.status == '10') {
              this.$router.push('/login');
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
  },
    created() {
      this.user_id = this.$route.params.user_id;
      this.check_confirm();
  },
};
</script>