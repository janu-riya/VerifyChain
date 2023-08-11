<template>
    <!-- ======= Features Section ======= -->
    <section id="features" class="services">
        <div class="container">
    
          <div class="section-title" data-aos="fade-up">
            <h2>Features</h2>
            <p>Magnam dolores commodi suscipit eius consequatur ex aliquid fug</p>
          </div>
    
          <div class="row">
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="100">
                <div class="icon">
                  <v-icon>mdi-security</v-icon>
                </div>
                <h4 class="title"><a href="">Blockchain-Backed Security</a></h4>
                <p class="description">Your data is secured using cutting-edge blockchain 
                          technology, providing an immutable and tamper-proof verification process.</p> 
                                                      
              </div>
            </div>
    
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="300">
                <div class="icon">
                  <v-icon>mdi-check-decagram</v-icon>
                </div>
                <h4 class="title"><a href=""> Individual User Verification</a></h4>
                <p class="description"> Empower individuals to verify their own documents 
                          effortlessly for future use. </p>
              </div>
            </div>
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
                <div class="icon">
                  <v-icon>mdi-file-upload</v-icon>
    
                </div>
                <h4 class="title"><a href="">Bulk Candidate Upload </a></h4>
                <p class="description">Hiring companies can upload candidate data in bulk, 
                          streamlining the verification process</p>
              </div>
            </div>
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
                <div class="icon">
                  <v-icon>mdi-folder-account</v-icon>
    
                </div>
                <h4 class="title"><a href="">Verified Candidate Showcase</a></h4>
                <p class="description">Hiring companies can view a status dashboard, 
    showcasing verified candidates ready for onboarding.
                    </p>
              </div>
            </div>
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
                <div class="icon">
                  <v-icon>mdi-close-octagon</v-icon>
    
                </div>
                <h4 class="title"><a href="">Automatic Rejection Handling</a></h4>
                <p class="description">If a document is rejected, the system prompts users to 
    reupload the corrected one. 
    </p>
              </div>
            </div>
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
                <div class="icon">
                  <v-icon>mdi-download-box</v-icon>
    
                </div>
                <h4 class="title"><a href="">Download Verified Documents</a></h4>
                <p class="description">Access and download your verified documents 
    anytime, anywhere for hassle-free sharing.</p>
              </div>
            </div>
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
                <div class="icon">
                  <v-icon>mdi-update</v-icon>
    
                </div>
                <h4 class="title"><a href="">Document Update Capability</a></h4>
                <p class="description"> Users can easily update their documents whenever 
    necessary, keeping their credentials current. </p>
              </div>
            </div>
    
            <div class="col-md-6 col-lg-3 d-flex align-items-stretch mb-5 mb-lg-0">
              <div class="icon-box" data-aos="fade-up" data-aos-delay="400">
                <div class="icon">
                  <v-icon>mdi-timelapse</v-icon>
    
                </div>
                <h4 class="title"><a href="">Real-time Status Updates</a></h4>
                <p class="description">Track the verification status of your documents in real-time, eliminating uncertainty. 
    
    </p>
              </div>
            </div>
    
            
    
          </div>
    
        </div>
      </section><!-- End Services Section -->
    

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

</style>