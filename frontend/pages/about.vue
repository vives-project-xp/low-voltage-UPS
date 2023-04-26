<template>
  <section>
    <PageTitle title="About" />
    <!-- Who are we? -->
    <div class="rounded-2xl tertiary-color-card mx-16">
      <div class="divider p-8 text-2xl font-bold text-center">Who are we ?</div>
      <div class="flex md:flex-row flex-col p-8 ">
            <div class=" md:w-1/2 md:mr-4 w-auto ms:mr-0">
                <img src="https://picsum.photos/id/176/500/400" alt="placeholder">
            </div>
            <div class="md:w-1/2 w-auto text-justify">
              <div >
                <div>
                  <span>
                    Lorem ipsum dolor, sit amet consectetur adipisicing elit. 
                    Temporibus nam cumque ex repellendus ratione molestiae, beatae nostrum est, 
                    iure iste, molestias aliquam placeat quibusdam dolorem voluptate voluptates illo tempore tempora.
                  </span>
                </div>
                <div>
                  <span>
                    Lorem ipsum dolor, sit amet consectetur adipisicing elit. 
                    Temporibus nam cumque ex repellendus ratione molestiae, beatae nostrum est, 
                    iure iste, molestias aliquam placeat quibusdam dolorem voluptate voluptates illo tempore tempora.
                  </span>
                </div>
                <div>
                  <span>
                    Lorem ipsum dolor, sit amet consectetur adipisicing elit. 
                    Temporibus nam cumque ex repellendus ratione molestiae, beatae nostrum est, 
                    iure iste, molestias aliquam placeat quibusdam dolorem voluptate voluptates illo tempore tempora.
                  </span>
                </div>
              </div>
            </div>
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
    {id: 0, name: 'Axel', avatar: 'https://picsum.photos/id/153/200', job: 'Hardware & Firmware'},
    {id: 1, name: 'Maxime', avatar: 'https://picsum.photos/id/172/200', job: 'Firmware'},
    {id: 2, name: 'Rob', avatar: 'https://picsum.photos/id/137/200', job: 'Website , Home Assistant device Integration'},
    {id: 3, name: 'Tibo', avatar: 'https://picsum.photos/id/155/200', job: 'Home Assistant Integration , Website'},
  ])
</script>