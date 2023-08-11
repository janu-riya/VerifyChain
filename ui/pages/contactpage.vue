<template>
    <section id="contact" class="contact">
        <div class="container">
    
          <div class="section-title" data-aos="fade-up">
            <h2>Contact Us</h2>
          </div>
          
    <v-container class="center">
    
        <v-container fluid fill-height>
        
        <v-card
        class="mx-auto"
        width="400"
        color="white">
        <h3 class="text-h6 text-center " style="padding:5%; color:black"> </h3>
        <v-container style="width: 100%;">
          <v-card-text style="color:black">
            <form ref="form" @submit.prevent="submit()"> 
              <v-text-field
                v-model="name"
                color="primary"
                label="Your name"
                variant="underlined">
              </v-text-field>
    
              <v-text-field
                v-model="email"
                color="primary"
                label="Email"
                variant="underlined">
              </v-text-field>
    
              <v-text-field
                v-model="subject"
                name="subject"
                label="Subject"
                variant="underlined">
              </v-text-field>
    
              <v-text-field
                v-model="message"
                name="message"
                label="Message"
                variant="underlined">
              </v-text-field>
    
            </form>
          </v-card-text>
        </v-container>
        <v-container class="text-center">
                    <v-btn rounded color="#3498db"> Send message</v-btn>  
                </v-container>
         
    
        
      </v-card>
    </v-container>
        </v-container>
          </div>
    
    
      </section><!-- End Contact Section -->
</template>
<script src="../assets/img/favicon.png" rel="icon"></script>
<script src="../assets/img/apple-touch-icon.png" rel="apple-touch-icon"></script>

<!-- Google Fonts -->
<script src="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">


<script src="../assets/vendor/aos/aos.css" rel="stylesheet"></script>
<script src="../assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet"></script>
<script src="../assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet"></script>
<script src="../assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet"></script>
<script src="../assets/vendor/glightbox/css/glightbox.min.css" rel="stylesheet"></script>
<script src="../assets/vendor/remixicon/remixicon.css" rel="stylesheet"></script>
<script src="../assets/vendor/swiper/swiper-bundle.min.css" rel="stylesheet"></script>

<!-- Template Main CSS File -->
<script src="../assets/css/style.css" rel="stylesheet"></script>

<style>
/*--------------------------------------------------------------
# Contact
--------------------------------------------------------------*/
.contact-contact.png{
    width:10%; padding-top: 20%;
  
  
  }
</style>