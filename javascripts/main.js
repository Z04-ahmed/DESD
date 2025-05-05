  // HOMEPAGE INTERACTIONS
  document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lucide icons
    // Assuming lucide is available globally or imported elsewhere.
    // If not, you'll need to import it:
    // import * as lucide from 'lucide';
    // or
    // const lucide = require('lucide'); // if using CommonJS
  
    lucide.createIcons()
  
    // Set current year in footer
    document.querySelectorAll("#current-year").forEach((el) => {
      el.textContent = new Date().getFullYear()
    })
  
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector(".mobile-menu-button")
    const mobileNav = document.querySelector(".mobile-nav")
  
    if (mobileMenuButton && mobileNav) {
      mobileMenuButton.addEventListener("click", function () {
        mobileNav.classList.toggle("active")
  
        // Toggle icon between menu and x
        const icon = this.querySelector("i")
        if (icon) {
          if (mobileNav.classList.contains("active")) {
            icon.setAttribute("data-lucide", "x")
          } else {
            icon.setAttribute("data-lucide", "menu")
          }
          lucide.createIcons()
        }
      })
    }
  
    // Testimonial slider
    const testimonialSlides = document.querySelectorAll(".testimonial-slide")
    const testimonialDots = document.querySelectorAll(".testimonial-dot")
    const prevButton = document.querySelector(".testimonial-prev")
    const nextButton = document.querySelector(".testimonial-next")
  
    if (testimonialSlides.length > 0) {
      let currentSlide = 0
  
      // Function to show a specific slide
      function showSlide(index) {
        // Hide all slides
        testimonialSlides.forEach((slide) => {
          slide.classList.remove("active")
        })
  
        // Deactivate all dots
        testimonialDots.forEach((dot) => {
          dot.classList.remove("active")
        })
  
        // Show the current slide and activate the corresponding dot
        testimonialSlides[index].classList.add("active")
        testimonialDots[index].classList.add("active")
  
        // Update current slide index
        currentSlide = index
      }
  
      // Next slide function
      function nextSlide() {
        const nextIndex = (currentSlide + 1) % testimonialSlides.length
        showSlide(nextIndex)
      }
  
      // Previous slide function
      function prevSlide() {
        const prevIndex = (currentSlide - 1 + testimonialSlides.length) % testimonialSlides.length
        showSlide(prevIndex)
      }
  
      // Set up event listeners for dots
      testimonialDots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
          showSlide(index)
        })
      })
  
      // Set up event listeners for prev/next buttons
      if (prevButton) {
        prevButton.addEventListener("click", prevSlide)
      }
  
      if (nextButton) {
        nextButton.addEventListener("click", nextSlide)
      }
  
      // Auto-advance slides every 5 seconds
      setInterval(nextSlide, 5000)
    }
  
    // Intersection Observer for fade-in animations
    const fadeElements = document.querySelectorAll(".feature-item, .feature-row, .section-title")
  
    if (fadeElements.length > 0 && "IntersectionObserver" in window) {
      const fadeObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("fade-in")
              fadeObserver.unobserve(entry.target)
            }
          })
        },
        { threshold: 0.1 },
      )
  
      fadeElements.forEach((element) => {
        element.classList.add("fade-element")
        fadeObserver.observe(element)
      })
    }
  })
  
  