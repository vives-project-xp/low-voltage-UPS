<template>
  <section>
    <PageTitle title="About" />
    <!-- Who are we? -->
    <div class="divider p-8 text-2xl font-bold text-center">Who are we ?</div>
    <div class="mx-8 flex bg-base-300">
      <img src="https://picsum.photos/id/176/500/400" alt="placeholder" class="p-8 w-1/3">
      <div class="p-8 w-2/3 flex flex-col justify-center">
        <p class="h-fit text-left">
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
          Assumenda et neque inventore tempore similique, ab iusto laborum, quasi dolorem, harum illo nam exercitationem quod magni doloremque?
          Quis in sint numquam?
        </p>
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