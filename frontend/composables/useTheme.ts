export default function useTheme() {
    const enabled = useState<boolean | null>('nuxt-color-mode', ()=>null)
  
    onMounted(()=>{
      enabled.value = localStorage.getItem("nuxt-color-mode") === "dark" ? true : false
    })
    
  
    const toggleTheme = () => {
      enabled.value = !enabled.value
      localStorage.setItem("nuxt-color-mode", enabled.value ? "dark" : "light")
      setTheme()
    }
  
    function setTheme() {
      const theme = localStorage.getItem("nuxt-color-mode")
      if (theme === "dark" || (!theme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
        document.documentElement.setAttribute("nuxt-color-mode", "dark")
        enabled.value = true
      } else {
        document.documentElement.removeAttribute("nuxt-color-mode")
        enabled.value = false
      }
    }
  
    return {
      enabled,
      toggleTheme,
      setTheme,
    }
  }