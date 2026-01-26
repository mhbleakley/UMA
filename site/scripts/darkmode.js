function updateThemeByTime() {
    const hour = new Date().getHours();
    const dark = (hour >= 17 || hour < 7);

    document.body.classList.toggle("dark", dark);
    // document.body.classList.add("dark");
    // document.body.classList.remove("dark");
    

}

updateThemeByTime();
console.log("This script ran");
setInterval(updateThemeByTime, 5 * 1000)