// Add bootstrap to images created with markdown
(() => {
  const images = document.getElementsByTagName("img");

  for (const image of images) {
    // Ignore items with 'no-styling' class
    if (image.classList[0] !== "no-styling") {
      image.className = "border rounded img-fluid";
    }
  }
})();

// On small screens have search on top of page
(() => {
  const boostrapSizeLg = 992;
  const postsElement = document.getElementById("posts");
  const sidebarElement = document.getElementById("sidebar");
  let isSwapped = false;

  if (!postsElement || !sidebarElement) {
    return;
  }

  const swapElements = (element1, element2) => {
    const copy = element2.cloneNode();

    element1.parentNode.insertBefore(copy, element1);
    element2.parentNode.insertBefore(element1, element2);
    element2.parentNode.replaceChild(element2, copy);
  };

  window.addEventListener("load", () => {
    if (window.innerWidth < boostrapSizeLg) {
      swapElements(postsElement, sidebarElement);
      isSwapped = true;
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth < boostrapSizeLg && !isSwapped) {
      swapElements(postsElement, sidebarElement);
      isSwapped = true;
    } else if (window.innerWidth >= boostrapSizeLg && isSwapped) {
      swapElements(postsElement, sidebarElement);
      isSwapped = false;
    }
  });
})();
