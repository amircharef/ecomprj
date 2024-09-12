// Slide Swiper
console.log("Checking top");

var swiper1 = new Swiper(".slide-swp", {
  pagination: {
    el: ".swiper-pagination",
    dynamicBullets: true,
    clickable: true
  },
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  loop: true,
});

// Deals Swiper
var swiper2 = new Swiper(".deals", {
  slidesPerView: 2,
  spaceBetween: 30,
  autoplay: {
    delay: 1000,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  loop: true,
  breakpoints: {
    1200: {
      slidesPerView: 2,
    },
    990: {
      slidesPerView: 1,
    },
    0: {
      slidesPerView: 1,
    }
  }
});

// Sale Section Swiper
var swiper3 = new Swiper(".sale-sec", {
  slidesPerView: 5,
  spaceBetween: 30,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  loop: true,
  breakpoints: {
    1400: {
      slidesPerView: 5,
    },
    1200: {
      slidesPerView: 4,
    },
    800: {
      slidesPerView: 3,
      spaceBetween: 30,
    },
    650: {
      slidesPerView: 3,
      spaceBetween: 15,
    },
    0: {
      slidesPerView: 2,
      spaceBetween: 10,
    }
  }
});

// Swiper with Images
var swiper4 = new Swiper(".swip-with-img", {
  slidesPerView: 4,
  spaceBetween: 30,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  loop: true,
  breakpoints: {
    1400: {
      slidesPerView: 4,
    },
    1100: {
      slidesPerView: 3,
    },
    800: {
      slidesPerView: 2,
      spaceBetween: 30,
    },
    700: {
      slidesPerView: 2,
      spaceBetween: 15,
    },
    0: {
      slidesPerView: 2,
      spaceBetween: 10,
    }
  }
});

document.addEventListener('DOMContentLoaded', function() {
  console.log("DOMContentLoaded event triggered");

  // Side bar toggle for responsive design
  let btnCloseSide = document.getElementById("btn-close");
  let sideBar = document.getElementById("side-bar");
  let btnOpenSide = document.getElementById("open-side");

  if (btnOpenSide && btnCloseSide && sideBar) {
    btnOpenSide.onclick = () => {
      sideBar.classList.add('active');
    }
    btnCloseSide.onclick = () => {
      sideBar.classList.remove('active');
    }
  } else {
    console.log("Sidebar elements not found");
  }

  // // Change big product image
  // let bigImage = document.getElementById('big-img');

  // if (bigImage) {
  //   function myProduct(item) {
  //     bigImage.src = item;
  //   }
  // } else {
  //   console.log("Big image element not found");
  // }

  // Buy fast order toggle
  // let btnbuyNowF = document.querySelector('.buyNow');
  // let divcretAcBuyF = document.querySelector('.creatacountfast');

  // if (btnbuyNowF && divcretAcBuyF) {
  //   btnbuyNowF.onclick = () => {
  //     divcretAcBuyF.classList.toggle('active');
  //   }
  // } else {
  //   console.log("Buy now elements not found");
  // }

  console.log("From main.js");

});