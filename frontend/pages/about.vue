<template>
  <section>
    <PageTitle title="About" />
    <!-- Who are we? -->
    <div class="rounded-2xl tertiary-color-card mx-16">
      <div class="divider p-8 text-2xl font-bold text-center">Who are we ?</div>
      <div class="flex md:flex-row flex-col px-8 ">
            <div class=" md:w-1/2 md:mr-4 w-auto ms:mr-0">
                <img src="https://picsum.photos/id/176/500/400" alt="placeholder">
            </div>
            <div class="md:w-1/2 w-auto text-justify">
              <div >
                <div>
                  <span>
                    Our team is composed of students from diverse backgrounds, 
                    all with a shared passion for using technology to create practical solutions to real-world problems.
                    We believe that by bringing together students with different skill sets and perspectives, 
                    we can approach challenges from multiple angles and develop creative solutions that are both effective and efficient.
                  </span>
                </div>
                <br>
                <div>
                  <span>
                    We work collaboratively to leverage each other's strengths and provide our clients with innovative solutions 
                    that are visually appealing, user-friendly,
                    and completed on time and within budget.
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="w-auto text-justify px-8">
            <span>
              At the core of our team is a commitment to exceptional customer service.
              We believe that building long-lasting relationships with our clients is the key to our success.
              We work closely with our clients to understand their needs and objectives, 
              and we keep them informed every step of the way. Our goal is to exceed our clients' expectations,
              and we take great pride in our ability to deliver high-quality results that meet their needs.
            </span>
          </div>
              
            
      <!-- Meet the team -->
      <div class="divider p-8 text-2xl font-bold text-center">Meet the team</div>
      <div class="mx-8 mb-8 flex flex-wrap justify-center gap-8">
        <AboutCard 
          v-for="person in team" 
          :key="person.id"
          :name="person.name"
          :avatar="person.avatar"
          :job="person.job"
          class="flex-1"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
  // team data
  const team = ref([
    {id: 0, name: 'Axel', avatar: '/img/axel.jpg', job: 'Hardware & Firmware'},
    {id: 1, name: 'Maxime', avatar: '/img/maxime.jpg', job: 'Firmware & hardware'},
    {id: 2, name: 'Rob', avatar: '/img/rob.jpg', job: 'Website , Home Assistant , device case'},
    {id: 3, name: 'Tibo', avatar: '/img/tibo.jpg', job: 'Home Assistant Integration , Website'},
  ])
</script>