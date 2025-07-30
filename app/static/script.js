const timerTag = document.querySelector("#timer");

const max_usage = 60 * 5; // in seconds
let timer = 0; // in seconds

window.addEventListener("DOMContentLoaded", (event) => {
  setInterval(() => {
    if (timer < max_usage) {
      timer += 1;

      let hrs = Math.floor(timer / (60 * 60));
      let mins = Math.floor((timer % (60 * 60)) / 60);

      let clock_format = `${hrs.toString().padStart(2, "0")}:${mins.toString().padStart(2, "0")}`;

      timerTag.innerText = clock_format;
    } else {
      timerTag.innerText = "Locked";
      timerTag.classList.add("locked");
    }
  }, 1000);
});
