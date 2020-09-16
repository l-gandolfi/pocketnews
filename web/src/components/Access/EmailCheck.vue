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
                  title="PockeNews - Email address checked!"
                >
                <br>
                </b-card>
              </div>
            </v-container>
          </div>
          <div class="container">
              <h2 id = 'message'> </h2>
          </div>
          <br>
        </v-flex>
      </v-layout>
    </div>
  </div>

</template>


<script>
import axios from 'axios'

export default {
  data () {
    return {
      user_id: '',
      all_ok: '',
    }
  },
  methods: {
      set_mail_checked() {
        
        const path = '/mail_checked';
        

        const payload = {
          user_id: this.user_id,
          op_id: 0,
        };
        axios.post(path, payload)
          .then((res) => {
            
            if (res.data.status == '13' || res.data.status == '10') {
              this.$router.push('/login');
            } else if (res.data.status == '14') {
              document.getElementById("message").innerHTML = 'You have used a old email send to a not current email address...'
              } else {
                document.getElementById("message").innerHTML = 'Your email address has been confirmed, now you can <a class="ml-2" href="/login">login</a> inside PocketNews Network!!'
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
      this.set_mail_checked();

  },
};
</script>