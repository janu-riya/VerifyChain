<template>
    <v-container>
    <section id="features" class="services">
      <div class="container">

        <div class="section-title" data-aos="fade-up">
          <h2>who need us</h2>
          <p> VerifiEdge is essential for individuals seeking hassle-free background checks and verified credentials, and for companies looking to streamline their hiring process with reliable talent. Join us today for a secure and efficient background verification experience.</p>
        </div>

        <div class="row">
          <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
            <div class="icon-box" data-aos="fade-up" data-aos-delay="100">
              <div class="icon">
                <v-icon>mdi-domain</v-icon>
              </div>              
              <h4 class="title"><a href="">Company</a></h4>
              <p class="description">Streamline hiring with bulk candidate details upload and real-time verification tracking.
Access a verified talent pool for efficient and reliable candidate onboarding.</p> 
<br>

                <v-btn rounded  to="/hrsignin">
                    signin
                </v-btn>     
                &ensp;
<v-btn size="20%" rounded to="/hrsignup">
    signup
</v-btn>                               
            </div>
          </div>
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;

          <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
            <div class="icon-box" data-aos="fade-up" data-aos-delay="300">
              <div class="icon">
                <v-icon>mdi-check-decagram-outline</v-icon>
              </div>
              <h4 class="title"><a href=""> Notary</a></h4>
              <p class="description"> Manage user data, documents, and verification progress from a centralized dashboard.
Oversee notary verification, blockchain integration, and real-time status tracking.
</p>
<br>
<v-btn rounded to="/notarysignin">
    signin

</v-btn>
&ensp;
<v-btn size="20%" rounded to="/notarysignup">
    signup
</v-btn>    
            </div>
          </div>
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          &ensp;
          

          <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
            <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
              <div class="icon">
                <v-icon>mdi-account</v-icon>
              </div>
              <h4 class="title"><a href="">User</a></h4>
              <p class="description">Easily upload documents, track verification status, and access verified credentials.
Benefit from secure document storage and blockchain-backed verification.
</p>
<br>
<v-btn size="20%" rounded to="/signin">
    signin
</v-btn>
&ensp;
<v-btn size="20%" rounded to="/signup">
    signup
</v-btn>
            </div>
          </div>

          
          

        </div>

      </div>
    </section><!-- End Services Section -->
    </v-container>
</template>
<script>
export default {
    name : 'Getstarted',
    layout: 'signinlayout',
    data: () => ({}),
    methods: {

      async hr() {
          this.$router.push("/hrsignin");
      },
      async agencies(){
        this.$router.push("/hrsignin");
      },
      async notary(){
        this.$router.push("/notarysignin");
      }
      },

}
</script>
 <!-- Favicons -->
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


<style scoped>

/**
* Template Name: Vesperr
* Updated: May 30 2023 with Bootstrap v5.3.0
* Template URL: https://bootstrapmade.com/vesperr-free-bootstrap-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

/*--------------------------------------------------------------
# General
--------------------------------------------------------------*/
body {
font-family: "Open Sans", sans-serif;
color: #444444;
}

a {
color: #3498db;
text-decoration: none;
}

a:hover {
color: #5faee3;
text-decoration: none;
}

h1,
h2,
h3,
h4,
h5,
h6 {
font-family: "Raleway", sans-serif;
}




/*--------------------------------------------------------------
# Features
--------------------------------------------------------------*/
.services .icon-box {
padding: 30px;
position: relative;
overflow: hidden;
background: #fff;
box-shadow: 0 0 29px 0 rgba(68, 88, 144, 0.12);
transition: all 0.3s ease-in-out;
border-radius: 8px;
z-index: 1;
}

.services .icon-box::before {
content: "";
position: absolute;
background: #e1f0fa;
right: -60px;
top: -40px;
width: 100px;
height: 100px;
border-radius: 50px;
transition: all 0.3s;
z-index: -1;
}

.services .icon-box:hover::before {
background: #3498db;
right: 0;
top: 0;
width: 100%;
height: 100%;
border-radius: 0px;
}

.services .icon {
margin: 0 auto 20px auto;
padding-top: 10px;
display: inline-block;
text-align: center;
border-radius: 50%;
width: 60px;
height: 60px;
background: #3498db;
transition: all 0.3s ease-in-out;
}

.services .icon i {
font-size: 36px;
line-height: 1;
color: #fff;
}

.services .title {
font-weight: 700;
margin-bottom: 15px;
font-size: 18px;
}

.services .title a {
color: #111;
}

.services .description {
font-size: 15px;
line-height: 28px;
margin-bottom: 0;
}

.services .icon-box:hover .title a,
.services .icon-box:hover .description {
color: #fff;
}

.services .icon-box:hover .icon {
background: #fff;
}

.services .icon-box:hover .icon i {
color: #3498db;
}

/*--------------------------------------------------------------
# More Services
--------------------------------------------------------------*/
.more-services {
padding-top: 20px;
}

.more-services .card {
border: 0;
padding: 160px 20px 20px 20px;
position: relative;
width: 100%;
background-size: cover;
background-repeat: no-repeat;
background-position: center center;
}

.more-services .card-body {
z-index: 10;
background: rgba(255, 255, 255, 0.9);
padding: 15px 30px;
box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.1);
transition: 0.3s;
transition: ease-in-out 0.4s;
border-radius: 5px;
}

.more-services .card-title {
font-weight: 700;
text-align: center;
margin-bottom: 15px;
}

.more-services .card-title a {
color: #222222;
}

.more-services .card-text {
color: #5e5e5e;
}

.more-services .read-more a {
color: #777777;
text-transform: uppercase;
font-weight: 600;
font-size: 12px;
transition: 0.4s;
}

.more-services .read-more a:hover {
text-decoration: underline;
}

.more-services .card:hover .card-body {
background: #3498db;
}

.more-services .card:hover .read-more a,
.more-services .card:hover .card-title,
.more-services .card:hover .card-title a,
.more-services .card:hover .card-text {
color: #fff;
}

</style>
