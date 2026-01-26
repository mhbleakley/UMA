function ordinal(n) {
    if (n % 100 >= 11 && n % 100 <= 13) return n + "th";
    switch (n % 10) {
        case 1: return n + "st";
        case 2: return n + "nd";
        case 3: return n + "rd";
        default: return n + "th";
    }
}

function updateDate() {
    const now = new Date();

    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const day = ordinal(now.getDate());
    const month = months[now.getMonth()];
    const year = now.getFullYear();

    let hour24 = now.getHours();
    let hour12 = hour24 % 12;
    if (hour12 === 0) hour12 = 12;

    const meridian = hour24 < 12 ? "Ante Meridiem" : "Post Meridiem";
    const hour = ordinal(hour12);

    const minute = ordinal(now.getMinutes());

    const text =
        "The " + minute + " Minute of the " +
        hour + " Hour " + meridian + " of the " +
        day + " Day of " + month + ", " + year + ", Common Era<br>";


    document.getElementById("date").innerHTML = text;
}

updateDate();
setInterval(updateDate, 10000);