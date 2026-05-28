(() => {
  const slider = document.querySelector("[data-slider]");
  const slides = Array.from(document.querySelectorAll("[data-slide]"));
  const dots = Array.from(document.querySelectorAll("[data-index]"));
  const container = document.querySelector(".feature-slider");

  if (!slider || slides.length === 0) return;

  let index = 0;
  let intervalId = null;
  const intervalMs = 4500;

  const setActive = (nextIndex) => {
    index = (nextIndex + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === index);
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle("is-active", i === index);
      dot.setAttribute("aria-selected", i === index ? "true" : "false");
    });
  };

  const play = () => {
    stop();
    intervalId = setInterval(() => setActive(index + 1), intervalMs);
  };

  const stop = () => {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  };

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const target = Number(dot.getAttribute("data-index"));
      setActive(target);
      play();
    });
  });

  container?.addEventListener("mouseenter", stop);
  container?.addEventListener("mouseleave", play);
  container?.addEventListener("focusin", stop);
  container?.addEventListener("focusout", play);

  setActive(0);
  play();
})();
