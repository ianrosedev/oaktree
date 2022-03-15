// Add bootstrap to images created with markdown
(() => {
  const images = document.getElementsByTagName("img");

  for (const image of images) {
    // Ignore items with 'no-styling' class
    if (image.classList[0] !== "no-styling") {
      image.className = "rounded img-fluid";
    }
  }
})();
